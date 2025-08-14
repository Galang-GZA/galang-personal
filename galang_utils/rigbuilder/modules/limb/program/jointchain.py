"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.base import LimbBaseNode


class LimbJointNode(LimbBaseNode):
    """
    LimbJointNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        types: List = None,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        # This will add joint string to types if not exsit yet
        # usable for creating joint a la carte
        if not role.JOINT in types:
            types.insert(0, role.JOINT)

        # pre-compute locator name
        super().__init__(guide, module, kinematics, types, position, orientation)

    def create(self):
        """
        Creates the Maya joint.
        """
        cmds.select(clear=True)
        jnt_node = cmds.joint(name=self, position=self.position, orientation=self.orientation)
        cmds.setAttr(f"{jnt_node}.side", self.module.side_id)
        return jnt_node


class LimbJointSet(List[LimbJointNode]):
    """
    LimbJointSet behaves like a list (consisting joints name) but also carries extra
    metadata (module, guides, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guides,
        module: ModuleInfo,
        kinematics: str,
        indexing: bool = False,
        sub: bool = False,
        positions: List = [],
        group_enabled: bool = True,
    ):
        super().__init__()

        # Pre compute group
        if group_enabled:
            self.group = LimbGroupNode(guides[0], module, kinematics, [role.JOINT, role.GROUP])

        # Pre compute joints
        for i, (guide, position) in enumerate(zip(guides, positions)):
            index = f"{i+1:02d}" if indexing is not None else None
            jnt_node = LimbJointNode(guide, module, kinematics, [index, role.JOINT], position)
            self.append(jnt_node)

        # Pre compute root and end sub joints
        if sub:
            self.sub_root = LimbJointNode(guide, module, kinematics, [role.ROOT, role.JOINT], positions[0])
            self.sub_end = LimbJointNode(guide, module, kinematics, [role.END, role.JOINT], positions[-1])

    def create(self):
        """
        Creates the Maya joints.
        """
        # Define and create top node
        top_node = self.group.create()

        # Create sub root and end joints
        if self.sub_root and self.sub_end:
            self.sub_root.create()
            self.sub_end.create()
            cmds.parent(self.sub_root, top_node)
            cmds.parent(self.sub_end, self.sub_root)
            top_node = self.sub_root

        # Create each joint & parent accordingly
        for jnt_node in self:
            jnt_node.create()
            if top_node:
                cmds.parent(jnt_node, top_node)

            # Joint chaining
            top_node = jnt_node

        # # Pre compute sub joints between current and next guide
        # for guide in guides:
        #     index = guides.index(guide)
        #     if index + 1 >= len(guides):
        #         continue

        #     next_guide = guides[index + 1]
        #     sub_jnts: List[LimbJointNode] = []
        #     root_pos, end_pos = guide.position, next_guide.position
        #     sub_divs = sub_count - 1

        #     for i in range(sub_count):
        #         ratio = i / sub_divs
        #         sub_position = [root_pos[n] + ratio * (end_pos[n] - root_pos[n]) for n in range(3)]
        #         jnt_node = LimbJointNode(guide, module, kinematics, index=i, position=sub_position)
        #         sub_jnts.append(jnt_node)

        #     self.append(sub_jnts)

        #     # Pre compute root and end sub joints ik
        #     self.sub_root.append(LimbJointNode(guide, module, kinematics, role.ROOT, position=root_pos))
        #     self.sub_end.append(LimbJointNode(guide, module, kinematics, role.END, position=end_pos))
