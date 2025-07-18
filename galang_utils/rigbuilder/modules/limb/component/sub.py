from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.constant.project import setup as P_SETUP

from galang_utils.rigbuilder.core.guide import ModuleInfo, GuideInfo
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat 
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlCreator

class LimbRollComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.groups: Dict = {}
        self.joints: Dict = {}
        self.handles: Dict = {}
        self.controls: Dict[GuideInfo, Dict [str, Dict [int, LimbControlCreator]]]= []
        self.format = LimbFormat(self.guide.side)

    def create(self):
        guides = self.module.guides + self.module.guides_end
        index_list = [(0, 1), (1, 2)]

        #
        # Step 0 : Create groups
        # Create top group
        sub_grp_top_name = self.format(self.guide.name_raw, level=P_ROLE.GROUP)
        sub_grp_top = cmds.group(em=True, n=sub_grp_top_name)
        self.groups[P_ROLE.GROUP] = sub_grp_top

        for root, end in index_list:
            guide_root = guides[root]
            guide_end = guides[end]
            print(guide_root.name, guide_end.name)

            # Create sub groups
            sub_grp_types = [P_ROLE.MAIN, P_ROLE.JNT, P_ROLE.CTRL, P_ROLE.DETAIL, P_ROLE.ROLL]
            sub_grp = LimbGroupCreator(sub_grp_types, self.module)
            sub_grp.create()
            self.groups[guide_root.name] = sub_grp.map

            sub_grp_main = self.groups[guide_root.name][P_ROLE.MAIN]
            sub_grp_jnt = self.groups[guide_root.name][P_ROLE.JNT]
            sub_grp_ctrl = self.groups[guide_root.name][P_ROLE.CTRL]
            sub_grp_roll = self.groups[guide_root.name][P_ROLE.ROLL]
            sub_grp_detail = self.groups[guide_root.name][P_ROLE.DETAIL]
            
            # Parent sub groups
            for type, grp in self.groups[guide_root]:
                # Parent control and joint group into main group
                if type in [P_ROLE.JNT, P_ROLE.CTRL]:
                    cmds.parent (grp, sub_grp_main)
                
                # Parent roll and detail group into control group
                if type in [P_ROLE.ROLL, P_ROLE.DETAIL]:
                    cmds.parent(grp, sub_grp_ctrl)

            #
            # Step 1 : Create ik joints for guide root and end
            for i, guide in enumerate([guide_root, guide_end]):
                cmds.select(clear=True)
                jnt_name = self.format.name(f'{guide_root.name_raw}_0{i+1}', P_ROLE.JNT)
                jnt = cmds.joint(n=jnt_name, position=guide.position, orientation=guide.orientation)
                self.joints[guide_root.name][P_ROLE.IK][i] = jnt

            jnt_root = self.joints[guide_root][P_ROLE.IK][0]
            jnt_end = self.joints[guide_root][P_ROLE.IK][1]

            cmds.parent(jnt_end, jnt_root)
            cmds.parent(jnt_root, sub_grp_jnt)

            # Get positions
            root_pos = cmds.xform(jnt_root, q=True, ws=True, t=True)
            end_pos = cmds.xform(jnt_end, q=True, ws=True, t=True)

            #
            # Step 2 : Create ik handle
            ik_handle_name = self.format.name(guide_root.name_raw, P_ROLE.IK, P_ROLE.ROLL)
            ik_solver_name = self.format.name(guide_root.name_raw, P_ROLE.IK, P_ROLE.ROLL, 'SCsolver')
            ik_handle= cmds.ikHandle(n=ik_handle_name, sj=jnt_root, ee=jnt_end, sol="ikSCsolver")[0]
            cmds.rename("effector1", ik_solver_name)
            cmds.parent(ik_handle, sub_grp_main)
            self.handles[guide_root.name] = ik_handle

            #
            # Step 3 : Create roll / details joints and controls
            LEN_INDEX = P_SETUP.LEN_DETAILS - 1
            for i in range(P_SETUP.LEN_DETAILS):
                cmds.select(clear=True)
                ratio = i / LEN_INDEX if LEN_INDEX != 0 else 0
                interp_pos = [root_pos[n] + ratio * (end_pos[n] - root_pos[n]) for n in range(3)]

                jnt_name = self.format.name(f"{guide_root.name_raw}_0{i+1}", P_ROLE.JNT)
                jnt = cmds.joint(n=jnt_name, position=interp_pos, orientation=guide_root.orientation)
                jnt_pos = cmds.xform(jnt, q=True, ws=True, t=True)

                cmds.parent(jnt, jnt_root)
                self.joints[f"{guide_root.name}{i}"] = jnt

                ctrl_roll = LimbControlCreator(guide_root, f"{P_ROLE.ROLL}{i+1}", self.module)
                ctrl_detail = LimbControlCreator(guide_root, f"{P_ROLE.DETAIL}{i+1}", self.module)

                for manipulator, type in zip([ctrl_roll, ctrl_detail], [P_ROLE.ROLL, P_ROLE.DETAIL]):
                    manipulator.create(color_set=P_SETUP.SUB_COLOR, node_level=P_SETUP.NODE_SUB_LEVELS)
                    cmds.xform(manipulator.top, ws=True, t=jnt_pos)

                    # Scale and parent controls
                    if type == P_ROLE.ROLL:
                        cmds.xform(manipulator.ctrl, s=[0.85, 0.85, 0.85])
                        cmds.parent (manipulator.top, sub_grp_roll)

                    if type == P_ROLE.DETAIL:
                        cmds.xform(manipulator.ctrl, s=[0.9, 0.9, 0.9])
                        cmds.parent (manipulator.top, sub_grp_detail)
                    
                    cmds.makeIdentity(manipulator.ctrl, a=True, s=1)
                    self.controls[guide_root][type][i] = manipulator
