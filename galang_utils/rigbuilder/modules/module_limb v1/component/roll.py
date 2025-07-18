from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.program.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.program.jointchain import LimbJointChainSetup


class LimbRollComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.groups: Dict = {}
        self.joints: Dict = {}
        self.controls: Dict[str, LimbControlCreator] = {}
        self.handles: Dict = {}

    def create(self):
        guides = self.module.guides + self.module.guides_end
        index_list = [(0, 1), (1, 2)]

        #
        # Step 0 : Create groups
        # Create master group
        grp_master_name = limb_format(PROJECT, ROLL, self.guide.side, self.guide.name_raw, GROUP)
        grp_master = cmds.group(em=True, n=grp_master_name)
        self.groups[MASTER] = grp_master

        for root, end in index_list:
            g_root = guides[root]
            g_end = guides[end]
            print(g_root.name, g_end.name)

            # Create main group
            grp_main_name = limb_format(PROJECT, ROLL, self.guide.side, g_root.name_raw, MAIN)
            grp_main = cmds.group(em=True, n=grp_main_name)
            cmds.parent(grp_main, grp_master)
            self.groups[f"{g_root.name}{MAIN}"] = grp_main

            # Create sub groups
            group_list = [JNT, CTRL, DETAIL, ROLL]
            for grp_typ in group_list:
                grp_name = limb_format(PROJECT, ROLL, self.guide.side, g_root.name_raw, grp_typ)
                grp = cmds.group(em=True, n=grp_name)
                self.groups[f"{g_root.name}{grp_typ}"] = grp

                # Parent control and joint group into main group
                if grp_typ in [JNT, CTRL]:
                    cmds.parent(grp, grp_main)

                # Parent control and joint group into main group
                if grp_typ in [DETAIL, ROLL]:
                    cmds.parent(grp, grp_main)

            #
            # Step 1 : Create ik joints for g_root.name and end
            for i, g in enumerate([g_root, g_end]):
                cmds.select(clear=True)
                jnt_name = limb_joint_format(PROJECT, f"{ROLL}_{IK}", g.side, f"{g_root.name_raw}_0{i+1}", JNT)
                jnt = cmds.joint(n=jnt_name, position=g.position, orientation=g.orientation)
                self.joints[f"{g_root.name}{IK}{i}"] = jnt

            jnt_root = self.joints[f"{g_root.name}{IK}0"]
            jnt_end = self.joints[f"{g_root.name}{IK}1"]

            cmds.parent(jnt_end, jnt_root)
            cmds.parent(jnt_root, self.groups[f"{g_root.name}{JNT}"])

            # Get positions
            root_pos = cmds.xform(jnt_root, q=True, ws=True, t=True)
            end_pos = cmds.xform(jnt_end, q=True, ws=True, t=True)
            LEN_INDEX = LEN_DETAILS - 1

            #
            # Step 2 : Create ik handle
            ik_handle_name = limb_format(PROJECT, f"{ROLL}_{IK}", self.guide.side, g_root.name_raw)
            ik_solver_name = limb_format(PROJECT, f"{ROLL}_{IK}", self.guide.side, g_root.name_raw, item="SCsolver")
            self.handles[g_root.name] = cmds.ikHandle(n=ik_handle_name, sj=jnt_root, ee=jnt_end, sol="ikSCsolver")[0]
            cmds.rename("effector1", ik_solver_name)
            cmds.parent(self.handles[g_root.name], self.groups[f"{g_root.name}{MAIN}"])

            #
            # Step 3 : Create roll / details joints and controls
            for index in range(LEN_DETAILS):
                cmds.select(clear=True)
                ratio = index / LEN_INDEX if LEN_INDEX != 0 else 0
                interp_pos = [root_pos[i] + ratio * (end_pos[i] - root_pos[i]) for i in range(3)]

                jnt_name = limb_joint_format(PROJECT, ROLL, g_root.side, f"{g_root.name_raw}_0{index+1}", JNT)
                jnt = cmds.joint(n=jnt_name, position=interp_pos, orientation=g_root.orientation)
                jnt_pos = cmds.xform(jnt, q=True, ws=True, t=True)

                cmds.parent(jnt, jnt_root)
                self.joints[f"{g_root.name}{index}"] = jnt

                ctrl_detail = LimbControlCreator(g_root, f"{DETAIL}{index+1}", self.module)
                ctrl_roll = LimbControlCreator(g_root, f"{ROLL}{index+1}", self.module)

                for ctrl, type in zip([ctrl_detail, ctrl_roll], [DETAIL, ROLL]):
                    ctrl.create(color_set=SUB_COLOR, node_level=NODE_SUB_LEVELS)
                    cmds.xform(ctrl.top, ws=True, t=jnt_pos)
                    cmds.parent(ctrl.top, self.groups[f"{g_root.name}{type}"])
                    if type == DETAIL:
                        cmds.xform(ctrl.ctrl, s=[0.9, 0.9, 0.9])
                    if type == ROLL:
                        cmds.xform(ctrl.ctrl, s=[0.85, 0.85, 0.85])
                    cmds.makeIdentity(ctrl.ctrl, a=True, s=1)
                    self.controls[f"{g_root.name}{type}{index}"] = ctrl
