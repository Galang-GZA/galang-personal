from maya import cmds
from typing import Dict, List

from DIG_Maya.core.curve import shapes_library as gen_shapes
from DIG_Maya.core.component.dag import Node
from DIG_Maya.core.component.dag import Node
from DIG_Maya.core.support.node import apply_index_to_labels


from RigXFrame.core.constant import role as xframe_role
from RigXFrame.core.constant import setup as xframe_setup
from RigXFrame.mod_zeta_x.constant import role as role
from RigXFrame.mod_zeta_x.constant import setup as setup
from RigXFrame.core.guide import GuideInfo, ModuleInfo


class ControlNode(Node):
    """
    LimbControlNode LimbControlNode behaves like a string (the Maya node name) but also carries extra
     metadata (guide, module, node hierarchy, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        labels: List,
        position: List[float],
        orientation: List[float],
        layout: Dict = setup.MAIN,
    ):
        self.guide = guide
        self.module = module
        self.labels = labels
        # pre-compute control name
        if role.CONTROL not in labels:
            labels.append(role.CONTROL)
        super().__init__(guide.base_name, module.side, labels, position, orientation)

        # Pre compute node levels
        self.group = Node(guide.base_name, module.side, labels + [role.GROUP])
        self.mirror = Node(guide.base_name, module.side, labels + [role.MIRROR])
        self.constraint = Node(guide.base_name, module.side, labels + [role.CONSTRAINT])
        self.link = Node(guide.base_name, module.side, labels + [role.LINK])
        self.SDK = Node(guide.base_name, module.side, labels + [role.SDK])
        self.offset = Node(guide.base_name, module.side, labels + [role.OFFSET])

        self.color_set: Dict = layout.get(xframe_role.COLOR)
        self.node_levels: List = layout.get(xframe_role.LEVEL)
        self.top = self.node_levels[-1]

        self.level_dictionary: Dict[str:Node] = {
            role.GROUP: self.group,
            role.MIRROR: self.mirror,
            role.CONSTRAINT: self.constraint,
            role.LINK: self.link,
            role.SDK: self.SDK,
            role.OFFSET: self.offset,
        }

    def create(self):
        """
        Creates the Maya control curve + node hierarchy.
        """
        # Creates a control curve with the appropriate level hierarchy and mirror transform if needed.
        if self.module.side_id == None or self.guide.position is None or self.guide.orientation is None:
            cmds.warning(f"Cannot creat control for this guide:{self.guide.base_name} lha~")
            return

        # Create control based on the shapes library or basic shapes
        shape_type = xframe_role.HINGES if role.PV in self.guide.base_name else self.module.type
        item_types_order = [role.SETTINGS, role.DETAIL, role.IK, role.FK]
        item_type = next((item for item in item_types_order if item in self.labels), None)
        shape_data = gen_shapes.SHAPES_LIBRARY.get(item_type, {}).get(shape_type) if item_type else None

        if shape_data:
            ctrl = cmds.curve(d=shape_data["degree"], p=shape_data["control_points"], name=self)
            cmds.xform(ctrl, s=(self.guide.size, self.guide.size, self.guide.size))
            cmds.makeIdentity(ctrl, a=True, t=1, r=1, s=1)

        else:
            circle_normal = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}
            # print(f"Defaulting {self.guide.base_name} to circle")
            ctrl = cmds.circle(n=self, normal=circle_normal.get(self.module.axis), ch=False, radius=self.guide.size)[0]

        attrs = ["visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self}.{attr}", lock=True, keyable=False, channelBox=False)

        # Apply color to the control
        shape = cmds.listRelatives(self, shapes=True)[0]
        color_id = self.color_set.get(self.module.side_id, setup.COLOR_INDEX["yellow"])
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        cmds.setAttr(f"{shape}.overrideColor", color_id)

        # Resize detail control
        if role.DETAIL in self.labels:
            cmds.xform(self, s=[0.85, 0.85, 0.85])
            cmds.makeIdentity(self, a=True, s=1)

        # Build hierarchy levels
        self.top_node = self
        for level in self.node_levels:
            node: Node = self.level_dictionary.get(level)
            node.create()

            # Mirror node handling
            if self.module.side_id == setup.MIRROR_SIDE_ID and level == role.MIRROR:
                if setup.MIRROR_SCALE:
                    mirror_data = xframe_setup.MIRROR_AXIS_DATA[setup.MIRROR_AXIS]
                    cmds.xform(node, ro=mirror_data["orientation"], s=mirror_data["scale"])

            # Parent lower node under this one
            cmds.parent(self.top_node, node)

            # If mirrored, apply 180-degree rotation & freeze
            if self.module.side_id == setup.MIRROR_SIDE_ID and level == role.MIRROR:
                if setup.MIRROR_SCALE:
                    cmds.xform(self.top_node, ro=mirror_data["orientation"])
                    cmds.makeIdentity(self.top_node, a=True, t=1, r=1, s=1)

            self.top_node = node

        # Final placement
        cmds.xform(self.top_node, ws=True, t=self.guide.position, ro=self.guide.orientation)


class ControlSet(List[ControlNode]):
    """
    A list of LimbControlNode with module/guide metadata + create().
    """

    def __init__(
        self,
        guides: List[GuideInfo],
        module: ModuleInfo,
        labels: List,
        layout: Dict = setup.MAIN,
        positions: List[List[float]] = None,
        orientations: List[List[float]] = None,
    ):
        self.labels = labels

        # Precompute group
        labels.append(role.CONTROL)
        group_labels = labels + [role.GROUP]
        self.group = Node(guides[0].base_name, module.side, group_labels, positions[0], orientations[0])

        # Pre compute controls
        for i, (guide, position, orientation) in enumerate(zip(guides, positions, orientations)):
            resolved_labels = apply_index_to_labels(labels, i)
            control = ControlNode(guide, module, resolved_labels, layout, position, orientation)
            self.append(control)

    def create(self):
        # Create group
        self.group.create()
        top_node = self.group

        # Create controls and parent them accordingly
        for control in self:
            control.create()
            cmds.parent(control.group, top_node)

            # FK Chaining
            if role.FK in self.labels:
                top_node = control
