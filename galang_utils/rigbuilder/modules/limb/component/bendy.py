from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.constant.project import setup as setup

from galang_utils.rigbuilder.core.guide import ModuleInfo, GuideInfo
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointSet
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlSet
from galang_utils.rigbuilder.modules.limb.program.locator import LimbLocatorNode


class LimbBendyComponent:
    def __init__(self, module: ModuleInfo, sub_divs: int):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides

        # Pre-compute group sub rig group node
        self.group = LimbGroupNode(self.guide, module, [role.SUB, role.RIG, role.GROUP])

        # Pre-compute upper details components
        upper_positions = self._get_sub_positions(self.guides[0], sub_divs)
        self.upper_guides = [self.guides[0]] * sub_divs
        self.upper_joints = LimbJointSet(self.upper_guides, module, role.DETAIL, True, upper_positions)
        self.upper_controls = LimbControlSet(self.upper_guides, module, role.DETAIL, True, upper_positions)
        self.upper_loc_handle = LimbLocatorNode()
        self.upper_handle = None

        # Pre-compute lower details components
        lower_positions = self._get_sub_positions(self.guides[1], sub_divs)
        self.lower_guides = [self.guides[1]] * sub_divs
        self.lower_joints = LimbJointSet(self.lower_guides, module, role.DETAIL, True, lower_positions)
        self.lower_controls = LimbControlSet(self.lower_guides, module, role.DETAIL, True, lower_positions)
        self.lower_loc_handle = None
        self.lower_handle = None

    def _get_sub_positions(self, guide: GuideInfo, sub_divs):
        index = self.guides.index(guide)
        if index + 1 >= len(self.guides):
            return

        root_pos = guide.position
        end_pos = self.guides[index].position
        for i in range(sub_divs):
            root_pos = guide
            ratio = i / sub_divs
            sub_position = [root_pos[n] + ratio * (end_pos[n] - root_pos[n]) for n in range(3)]

        return sub_position

    def create(self):
        # Create pre-computed components
        self.group.create()
        self.upper_joints.create()
        self.upper_controls.create()
        self.lower_joints.create()
        self.lower_controls.create()
        # guides = self.module.guides + self.module.guides_end
        # index_list = [(0, 1), (1, 2)]

        # #
        # # Step 0 : Create groups
        # # Create top group
        # sub_grp_top_name = self.format(self.guide.name_raw, level=role.GROUP)
        # sub_grp_top = cmds.group(em=True, n=sub_grp_top_name)
        # self.groups[role.GROUP] = sub_grp_top

        # for root, end in index_list:
        #     guide_root = guides[root]
        #     guide_end = guides[end]
        #     print(guide_root.name, guide_end.name)

        #     # Create sub groups
        #     sub_grp_types = [role.MAIN, role.JOINT, role.CONTROL, role.DETAIL, role.ROLL]
        #     sub_grp = LimbGroup(sub_grp_types, self.module)
        #     sub_grp.create()
        #     self.groups[guide_root.name] = sub_grp.map

        #     sub_grp_main = self.groups[guide_root.name][role.MAIN]
        #     sub_grp_jnt = self.groups[guide_root.name][role.JOINT]
        #     sub_grp_ctrl = self.groups[guide_root.name][role.CONTROL]
        #     sub_grp_roll = self.groups[guide_root.name][role.ROLL]
        #     sub_grp_detail = self.groups[guide_root.name][role.DETAIL]

        #     # Parent sub groups
        #     for type, grp in self.groups[guide_root]:
        #         # Parent control and joint group into main group
        #         if type in [role.JOINT, role.CONTROL]:
        #             cmds.parent(grp, sub_grp_main)

        #         # Parent roll and detail group into control group
        #         if type in [role.ROLL, role.DETAIL]:
        #             cmds.parent(grp, sub_grp_ctrl)

        #     #
        #     # Step 1 : Create ik joints for guide root and end
        #     for i, guide in enumerate([guide_root, guide_end]):
        #         cmds.select(clear=True)
        #         jnt_name = self.format.name(f"{guide_root.name_raw}_0{i+1}", role.JOINT)
        #         jnt = cmds.joint(n=jnt_name, position=guide.position, orientation=guide.orientation)
        #         self.joints[guide_root.name][role.IK][i] = jnt

        #     jnt_root = self.joints[guide_root][role.IK][0]
        #     jnt_end = self.joints[guide_root][role.IK][1]

        #     cmds.parent(jnt_end, jnt_root)
        #     cmds.parent(jnt_root, sub_grp_jnt)

        #     # Get positions
        #     root_pos = cmds.xform(jnt_root, q=True, ws=True, t=True)
        #     end_pos = cmds.xform(jnt_end, q=True, ws=True, t=True)

        #     #
        #     # Step 2 : Create ik handle
        #     ik_handle_name = self.format.name(guide_root.name_raw, role.IK, role.ROLL)
        #     ik_solver_name = self.format.name(guide_root.name_raw, role.IK, role.ROLL, "SCsolver")
        #     ik_handle = cmds.ikHandle(n=ik_handle_name, sj=jnt_root, ee=jnt_end, sol="ikSCsolver")[0]
        #     cmds.rename("effector1", ik_solver_name)
        #     cmds.parent(ik_handle, sub_grp_main)
        #     self.handles[guide_root.name] = ik_handle

        #     #
        #     # Step 3 : Create roll / details joints and controls
        #     LEN_INDEX = setup.LEN_DETAILS - 1
        #     for i in range(setup.LEN_DETAILS):
        #         cmds.select(clear=True)
        #         ratio = i / LEN_INDEX if LEN_INDEX != 0 else 0
        #         interp_pos = [root_pos[n] + ratio * (end_pos[n] - root_pos[n]) for n in range(3)]

        #         jnt_name = self.format.name(f"{guide_root.name_raw}_0{i+1}", role.JOINT)
        #         jnt = cmds.joint(n=jnt_name, position=interp_pos, orientation=guide_root.orientation)
        #         jnt_pos = cmds.xform(jnt, q=True, ws=True, t=True)

        #         cmds.parent(jnt, jnt_root)
        #         self.joints[f"{guide_root.name}{i}"] = jnt

        #         ctrl_roll = LimbControlCreator(guide_root, f"{role.ROLL}{i+1}", self.module)
        #         ctrl_detail = LimbControlCreator(guide_root, f"{role.DETAIL}{i+1}", self.module)

        #         for manipulator, type in zip([ctrl_roll, ctrl_detail], [role.ROLL, role.DETAIL]):
        #             manipulator.create(color_set=setup.SUB_COLOR, node_level=setup.NODE_SUB_LEVELS)
        #             cmds.xform(manipulator.top, ws=True, t=jnt_pos)

        #             # Scale and parent controls
        #             if type == role.ROLL:
        #                 cmds.xform(manipulator.ctrl, s=[0.85, 0.85, 0.85])
        #                 cmds.parent(manipulator.top, sub_grp_roll)

        #             if type == role.DETAIL:
        #                 cmds.xform(manipulator.ctrl, s=[0.9, 0.9, 0.9])
        #                 cmds.parent(manipulator.top, sub_grp_detail)

        #             cmds.makeIdentity(manipulator.ctrl, a=True, s=1)
        #             self.controls[guide_root][type][i] = manipulator
