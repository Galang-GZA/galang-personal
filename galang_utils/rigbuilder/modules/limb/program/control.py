from maya import cmds
from typing import Dict, List
from galang_utils.curve import shapes_library as general_shapes
from galang_utils.rigbuilder.constant.general import role as general_role
from galang_utils.rigbuilder.constant.general import setup as general_setup
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.constant.project import setup as setup

from galang_utils.rigbuilder.modules.limb.constant import setup as limb_setup

from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode
from galang_utils.rigbuilder.modules.limb.program.locator import LimbLocatorNode

from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.base import LimbBaseNode


class LimbControlNode(LimbBaseNode):
    """
    LimbControlNode behaves like a string (the Maya node name) but also carries extra
    metadata (guide, module, node hierarchy, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        types: List,
        index: int,
        layout: Dict = setup.MAIN,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        super().__init__(guide, module, kinematics, types, position, orientation)

        self.color_set: Dict = layout.get(general_role.COLOR)
        self.node_levels: List = layout.get(general_role.LEVEL)
        self.nolde_level_flags: Dict = limb_setup.NODE_LEVEL_FLAGS

        # Pre compute node levels
        self.group = LimbGroupNode(guide, module, kinematics, [index, role.GROUP])
        self.mirror = LimbGroupNode(guide, module, kinematics, [index, role.MIRROR])
        self.constraint = LimbGroupNode(guide, module, kinematics, [index, role.CONSTRAINT])
        self.link = LimbGroupNode(guide, module, kinematics, [index, role.LINK])
        self.SDK = LimbGroupNode(guide, module, kinematics, [index, role.SDK])
        self.offset = LimbGroupNode(guide, module, kinematics, [index, role.OFFSET])
        self.space_locator = LimbLocatorNode(guide, module, kinematics, [index, role.LOCATOR, role.SPACE])

        self.level_nodes: list[LimbGroupNode] = [
            self.offset,
            self.SDK,
            self.link,
            self.constraint,
            self.mirror,
            self.group,
        ]

    def create(self):
        """
        Creates the Maya control curve + node hierarchy.
        """
        # Creates a control curve with the appropriate level hierarchy and mirror transform if needed.
        if self.module.side_id == None or self.guide.position is None or self.guide.orientation is None:
            cmds.warning(f"Cannot creat control for this guide:{self.guide.name_raw} lha~")
            return

        # Create control based on the shapes library or basic shapes
        if role.PV in self.guide.name:
            shape_type = general_role.HINGES
        else:
            shape_type = self.module.type
        shape_data = general_shapes.SHAPES_LIBRARY.get(self.kinematics, {}).get(shape_type)

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

        # Create space locators
        self.space_locator.create()
        cmds.parent(self.space_locator, self)

        # Build hierarchy levels
        top_node = self
        for level, node in zip(self.node_levels, self.level_nodes):
            if self.nolde_level_flags.get(level):
                cmds.select(clear=True)
                node.create()

                # Mirror node handling
                if self.module.side_id == setup.MIRROR_SIDE_ID and level == role.MIRROR:
                    if setup.MIRROR_SCALE:
                        mirror_data = general_setup.MIRROR_AXIS_DATA[setup.MIRROR_AXIS]
                        cmds.xform(node, ro=mirror_data["orientation"], s=mirror_data["scale"])

                # Parent lower node under this one
                cmds.parent(top_node, node)

                # If mirrored, apply 180-degree rotation & freeze
                if self.module.side_id == setup.MIRROR_SIDE_ID and level == role.MIRROR:
                    if setup.MIRROR_SCALE:
                        cmds.xform(top_node, ro=mirror_data["orientation"])
                        cmds.makeIdentity(top_node, a=True, t=1, r=1, s=1)

                top_node = node

        # Final placement
        cmds.xform(top_node, ws=True, t=self.guide.position, ro=self.guide.orientation)


class LimbControlSet(List[LimbControlNode]):
    """
    A list of LimbControlNode with module/guide metadata + create().
    """

    def __init__(
        self,
        guides: List[GuideInfo],
        module: ModuleInfo,
        kinematics: str,
        Bendy=False,
        positions: List = [],
        layout: Dict = setup.MAIN,
    ):
        self.kinematics = kinematics
        self.group: LimbGroupNode = None
        self.sub_groups: List[LimbGroupNode] = []

        # Pre compute controls and group
        group_type = [role.CONTROL, role.GROUP]
        self.group = LimbGroupNode(guides[0], module, kinematics, group_type)
        for i, (guide, position) in enumerate(zip(guides, positions)):
            index = None if Bendy is None else f"{i+1:02d}"
            control_type = [index, role.CONTROL]
            ctrl_node = LimbControlNode(guide, module, kinematics, control_type, index, layout, position)
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

            # Resize detail control
            if self.kinematics == role.DETAIL:
                cmds.xform(ctrl_node, s=[0.85, 0.85, 0.85])
                cmds.makeIdentity(ctrl_node, a=True, s=1)

            # Parent to group
            if top_node:
                cmds.parent(ctrl_node.group, top_node)

            # FK Chaining
            if self.kinematics == role.FK:
                top_node = ctrl_node
