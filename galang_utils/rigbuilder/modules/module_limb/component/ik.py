from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.program.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.program.jointchain import LimbJointChainSetup


class LimbIKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.map: Dict[GuideInfo, Dict[str, Union[LimbControlCreator, str]]] = {}
        self.handle: str = None
        self.group_map: Dict = {}
        self.comp_static_map: Dict = {}
        self.comp_active_map: Dict = {}

    def _create_loc_and_dist(self, name: str, dist_name: str, pos, parent_loc: str, parent_dist: str):
        loc = cmds.spaceLocator(n=name, p=pos)[0]
        dist = cmds.rename(cmds.createNode("distanceDimShape"), dist_name)
        cmds.parent(loc, parent_loc)
        cmds.parent(dist, parent_dist)
        return loc, dist

    def create(self):
        # Step 0: Create IK module groups
        group_master_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, GROUP)
        group_dnt_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, DNT)
        group_loc_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, LOCATOR)
        group_dist_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, DISTANCE)

        grp_name_list = [group_master_name, group_dnt_name, group_loc_name, group_dist_name]
        grp_type_list = [MASTER, DNT, LOCATOR, DISTANCE]

        for name, typ in zip(grp_name_list, grp_type_list):
            if not cmds.objExists(name):
                grp = cmds.group(em=True, n=name)
                self.group_map[typ] = grp
            else:
                cmds.warning(f"{name} already exists. Skipping")

        grp_master = self.group_map.get(MASTER)
        grp_dnt = self.group_map.get(DNT)
        grp_loc = self.group_map.get(LOCATOR)
        grp_dist = self.group_map.get(DISTANCE)

        if not all([grp_master, grp_dnt, grp_loc, grp_dist]):
            cmds.error("Missing one or more required groups")

        # Step 1 : Create IK joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name, IK)
        ik_joint_chain.build()
        cmds.parent(ik_joint_chain.group, grp_dnt)

        # Step 2 : Create IK controls
        for index, guide in enumerate(self.module.guides + self.module.guides_end):
            if index == 1:
                guide_obj = self.module.guides_pv[0]
                loc_pos = self.module.guides_pv[0].position
            else:
                guide_obj = guide
                loc_pos = guide.position

            ik_control = LimbControlCreator(guide_obj, IK, self.module)
            ik_control.create()
            cmds.parent(ik_control.top, grp_master)

            # Map IK controls and joints
            ik_joint = ik_joint_chain.output.get(guide.name)
            self.map[guide.name] = {CTRL: ik_control, JNT: ik_joint}

            # Step 3 : Create static distance and locator for soft feature and map them
            comp_sets = [
                (self.comp_static_map, LOCATOR, DISTANCE, guide.position),
                (self.comp_active_map, LOCATOR, DISTANCE, loc_pos),
            ]

            # Additional misc for index 2
            if index == 2:
                types = [SOFT, BASE, BLEND]
                for type in types:
                    comp_sets.append((self.comp_active_map, f"{LOCATOR}_{type}", f"{DISTANCE}_{type}", loc_pos))

            for comp_map, loc_key, dist_key, pos in comp_sets:
                loc_name = limb_format(PJ, RESULT, guide.side, guide.name_raw, item=loc_key)
                dist_name = limb_format(PJ, RESULT, guide.side, guide.name_raw, item=dist_key)
                loc, dist = self._create_loc_and_dist(loc_name, dist_name, pos, grp_loc, grp_dist)

                # Map locators and distances
                comp_map.setdefault(guide.name, {})
                comp_map[guide.name][loc_key] = loc
                comp_map[guide.name][dist_key] = dist

        # Step 5 : Create IK handle
        ik_handle_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None)
        ik_solver_name = limb_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None, item="RPsolver")
        self.handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=self.map[self.module.guides[0].name][JNT],
            ee=self.map[self.module.guides_end[0].name][JNT],
            sol="ikRPsolver",
        )[0]
        cmds.rename("effector1", ik_solver_name)
        cmds.parent(self.handle, self.map[self.module.guides_end[0].name][CTRL].ctrl)
        cmds.poleVectorConstraint(self.map[self.module.guides[1].name][CTRL].ctrl, self.handle)
