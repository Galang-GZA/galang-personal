from maya import cmds
from typing import Dict, List
from curve import shapes_library as gen_shapes
from rigbuilder.constant.general import role as gen_role
from rigbuilder.constant.general import setup as general_setup
from rigbuilder.constant.project import role as role
from rigbuilder.constant.project import setup as setup

from rigbuilder.modules.limb.constant import setup as limb_setup

from rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.locator import LocatorNode

from rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node


class ControlNode(Node):
    """
    LimbControlNode LimbControlNode behaves like a string (the Maya node name) but also carries extra
     metadata (guide, module, node hierarchy, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List,
        layout: Dict = setup.MAIN,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        # pre-compute control name
        control_types = types.append(role.CONTROL)
        super().__init__(guide, module, control_types, position, orientation)

        # Pre compute node levels
        self.group = GroupNode(guide, module, types.append(role.GROUP))
        self.mirror = GroupNode(guide, module, types.append(role.MIRROR))
        self.constraint = GroupNode(guide, module, types.append(role.CONSTRAINT))
        self.link = GroupNode(guide, module, types.append(role.LINK))
        self.SDK = GroupNode(guide, module, types.append(role.SDK))
        self.offset = GroupNode(guide, module, types.append(role.OFFSET))

        self.color_set: Dict = layout.get(gen_role.COLOR)
        self.node_levels: List = layout.get(gen_role.LEVEL)
        self.top = self.node_levels[-1]

        self.level_dictionary: Dict[str:GroupNode] = {
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
            cmds.warning(f"Cannot creat control for this guide:{self.guide.name_raw} lha~")
            return

        # Create control based on the shapes library or basic shapes
        shape_type = gen_role.HINGES if role.PV in self.guide.name else self.module.type
        item_types_order = [role.SETTINGS, role.DETAIL, role.IK, role.FK]
        item_type = next((item for item in item_types_order if item in self.types), None)
        shape_data = gen_shapes.SHAPES_LIBRARY.get(item_type, {}).get(shape_type) if item_type else None

        if shape_data:
            ctrl = cmds.curve(d=shape_data["degree"], p=shape_data["control_points"], name=self)
            cmds.xform(ctrl, s=(self.guide.size, self.guide.size, self.guide.size))
            cmds.makeIdentity(ctrl, a=True, t=1, r=1, s=1)

        else:
            circle_normal = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}
            # print(f"Defaulting {self.guide.name} to circle")
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
        if role.DETAIL in self.types:
            cmds.xform(self, s=[0.85, 0.85, 0.85])
            cmds.makeIdentity(self, a=True, s=1)

        # Build hierarchy levels
        self.top_node = self
        for level in self.node_levels:
            node: GroupNode = self.level_dictionary.get(level)
            node.create()

            # Mirror node handling
            if self.module.side_id == setup.MIRROR_SIDE_ID and level == role.MIRROR:
                if setup.MIRROR_SCALE:
                    mirror_data = general_setup.MIRROR_AXIS_DATA[setup.MIRROR_AXIS]
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
        types: List,
        layout: Dict = setup.MAIN,
        positions: List = [],
    ):
        self.types = types
        # Pre compute controls and group
        self.group = GroupNode(guides[0], module, types.append(role.GROUP))
        for i, (guide, position) in enumerate(zip(guides, positions)):
            i = f"{i+1:02d}"
            resolved_types = [(i if t is setup.INDEX else t) for t in types]
            ctrl_node = ControlNode(guide, module, [resolved_types], layout, position)
            self.append(ctrl_node)

    def create(self):
        """
        Creates the Maya controls.
        """
        # Create each joint & parent accordingly
        self.group.create()
        top_node = self.group

        for ctrl_node in self:
            ctrl_node.create()

            # Parent to group
            if top_node:
                cmds.parent(ctrl_node.group, top_node)

            # FK Chaining
            if role.FK in self.types:
                top_node = ctrl_node
