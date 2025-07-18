from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
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
        self.groups: Dict = {}
        self.comp_static_map: Dict = {}
        self.comp_active_map: Dict = {}

    def _create_loc_and_dist(self, name: str, dist_name: str, pos, rot, parent_loc: str, parent_dist: str):
        loc = cmds.spaceLocator(n=name)[0]
        dist = cmds.rename(cmds.createNode("distanceDimShape"), f"{dist_name}_shape")
        dist_transform = cmds.rename("distanceDimension1", dist_name)
        cmds.xform(loc, ws=True, t=pos, ro=rot)
        cmds.parent(loc, parent_loc)
        cmds.parent(dist_transform, parent_dist)
        return loc, dist

    def create(self):
        print(f"update {self.module.guide.name} success")
        # Step 0: Create IK module groups
        group_master_name = limb_format(PROJECT, IK, self.guide.side, self.guide.name_raw, GROUP)
        group_loc_name = limb_format(PROJECT, IK, self.guide.side, self.guide.name_raw, LOCATOR)
        group_dist_name = limb_format(PROJECT, IK, self.guide.side, self.guide.name_raw, DISTANCE)

        grp_name_list = [group_master_name, group_loc_name, group_dist_name]
        grp_type_list = [MASTER, LOCATOR, DISTANCE]

        for name, typ in zip(grp_name_list, grp_type_list):
            if not cmds.objExists(name):
                grp = cmds.group(em=True, n=name)
                self.groups[typ] = grp
            else:
                cmds.warning(f"{name} already exists. Skipping")
            if typ in [LOCATOR, DISTANCE]:
                cmds.hide(grp)

        grp_master = self.groups.get(MASTER)
        grp_loc = self.groups.get(LOCATOR)
        grp_dist = self.groups.get(DISTANCE)

        if not all([grp_master, grp_loc, grp_dist]):
            cmds.error("Missing one or more required groups")

        # Step 1 : Create IK joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name, IK)
        ik_joint_chain.build()
        cmds.parent(ik_joint_chain.group, self.groups[MASTER])
        self.groups[JNT] = ik_joint_chain.group

        # Step 2 : Create IK controls
        guides = self.module.guides + self.module.guides_end
        for index, guide in enumerate(guides):
            if index == 1:
                guide_obj = self.module.guides_pv[0]
                loc_pos = self.module.guides_pv[0].position
            else:
                guide_obj = guide
                loc_pos = guide.position

            ik_control = LimbControlCreator(guide_obj, IK, self.module)
            ik_control.create()
            cmds.addAttr(ik_control.ctrl, ln=FEATURES, at="enum", en="-", keyable=False)
            cmds.setAttr(f"{ik_control.ctrl}.{FEATURES}", e=True, cb=True)
            cmds.parent(ik_control.top, grp_master)

            # Map IK controls and joints
            ik_joint = ik_joint_chain.output.get(guide.name)
            self.map[guide.name] = {CTRL: ik_control, JNT: ik_joint}

            # Step 3 : Create static distance and locator for soft feature and map them
            comp_sets = [
                (self.comp_static_map, f"{LOCATOR}", f"{DISTANCE}", guide.position, guide.orientation, STATIC),
                (self.comp_active_map, f"{LOCATOR}", f"{DISTANCE}", loc_pos, guide.orientation, ACTIVE),
            ]

            # Additional misc for index 2
            if index == 2:
                types = [STRETCH, BASE, BLEND]
                for type in types:
                    comp_sets.append(
                        (
                            self.comp_active_map,
                            f"{LOCATOR}_{type}",
                            f"{DISTANCE}_{type}",
                            loc_pos,
                            guide.orientation,
                            "",
                        )
                    )

                # Add attributes for soft, stretch, pin, slide
                attrs = {
                    SOFT: [0.0001, 100, 0.0001],
                    STRETCH: [0.0, 1.0, 0.0],
                    PIN: [0.0, 1.0, 0.0],
                    SLIDE: [-1.0, 1.0, 0.0],
                }
                for attr, (min_val, max_val, default_val) in attrs.items():
                    if not cmds.attributeQuery(attr, node=ik_control.ctrl, exists=True):
                        cmds.addAttr(
                            ik_control.ctrl,
                            ln=attr,
                            at="double",
                            dv=default_val,
                            keyable=True,
                            min=min_val,
                            max=max_val,
                        )

            for comp_map, loc_key, dist_key, pos, rot, movement in comp_sets:
                loc_name = limb_format(
                    PROJECT, IK, f"{guide.side}_{movement}".strip("_"), guide.name_raw, item=loc_key
                )
                dist_name = limb_format(
                    PROJECT, IK, f"{guide.side}_{movement}".strip("_"), guide.name_raw, item=dist_key
                )
                loc, dist = self._create_loc_and_dist(loc_name, dist_name, pos, rot, grp_loc, grp_dist)

                # Map locators and distances
                comp_map.setdefault(guide.name, {})
                comp_map[guide.name][loc_key] = loc
                comp_map[guide.name][dist_key] = dist

        # Step 4 : Parent locators to destignated parent
        active0 = self.comp_active_map[guides[0].name]
        active2 = self.comp_active_map[guides[2].name]

        # Parent active end locator to a link group
        active2[LOCATOR_GROUP] = cmds.group(n=f"{active2[LOCATOR]}_{LINK}", em=True)
        cmds.xform(active2[LOCATOR_GROUP], ws=True, t=guides[2].position, ro=guides[2].orientation)
        cmds.parent(active2[LOCATOR], active2[LOCATOR_GROUP])

        # Step 5 : Create IK handle
        ik_handle_name = limb_format(PROJECT, IK, self.guide.side, self.guide.name_raw)
        ik_solver_name = limb_format(PROJECT, IK, self.guide.side, self.guide.name_raw, item="RPsolver")
        self.handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=self.map[self.module.guides[0].name][JNT],
            ee=self.map[self.module.guides_end[0].name][JNT],
            sol="ikRPsolver",
        )[0]

        cmds.rename("effector1", ik_solver_name)
        cmds.setAttr("ikRPsolver.tolerance", 1e-007)
        cmds.parent(self.handle, self.map[self.module.guides_end[0].name][CTRL].ctrl)
        cmds.poleVectorConstraint(self.map[self.module.guides[1].name][CTRL].ctrl, self.handle)
