from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.project import role as TASK_ROLE
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat 

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlCreator
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointChainSetup


class LimbIKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.groups: Dict = {}
        self.joints: List = []
        self.controls: List[LimbControlCreator] = []
        self.handle: str = None
        self.static_comps: Dict = {}
        self.active_comps: Dict = {}
        self.format = LimbFormat(self.guide.side, TASK_ROLE.IK)
        
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
        ik_grp_types = [TASK_ROLE.TOP, TASK_ROLE.LOCATOR, TASK_ROLE.DISTANCE]
        ik_grp = LimbGroupCreator(ik_grp_types, self.module)
        ik_grp.create()
        self.groups = ik_grp.map

        ik_grp_top = self.groups.get(TASK_ROLE.TOP)
        ik_grp_loc = self.groups.get(TASK_ROLE.LOCATOR)
        ik_grp_dist = self.groups.get(TASK_ROLE.DISTANCE)

        if not all([ik_grp_top, ik_grp_loc, ik_grp_dist]):
            cmds.error("Missing one or more required groups")

        # Step 1 : Create IK joint chain
        ik_jnt = LimbJointChainSetup(self.guide.name, TASK_ROLE.IK)
        ik_jnt.create()
        self.joints = ik_jnt.output
        self.groups[TASK_ROLE.JNT] = ik_jnt.group
        cmds.parent(self.groups[TASK_ROLE.JNT], ik_grp_top)

        # Step 2 : Create IK controls
        for index, guide in enumerate(self.guides):
            if index == 1:
                guide_obj = self.module.guides_pv[0]
                loc_position = self.module.guides_pv[0].position
            else:
                guide_obj = guide
                loc_position = guide.position

            ik_manipulator = LimbControlCreator(guide_obj, TASK_ROLE.IK, self.module)
            ik_manipulator.create()
            cmds.addAttr(ik_manipulator.ctrl, ln=TASK_ROLE.FEATURES, at="enum", en="-", keyable=False)
            cmds.setAttr(f"{ik_manipulator.ctrl}.{TASK_ROLE.FEATURES}", e=True, cb=True)
            cmds.parent(ik_manipulator.top, ik_grp_top)

            # Fill up FK controls
            self.controls.append(ik_manipulator)

            # Step 3 : Create static distance and locator for soft feature and map them
            comp_sets = [
                (self.static_comps, TASK_ROLE.LOCATOR, TASK_ROLE.DISTANCE, guide.position, guide.orientation, TASK_ROLE.STATIC),
                (self.active_comps, TASK_ROLE.LOCATOR, TASK_ROLE.DISTANCE, loc_position, guide.orientation, TASK_ROLE.ACTIVE),
            ]

            # Additional nodes for index 2
            if index == 2:
                types = [TASK_ROLE.STRETCH, TASK_ROLE.BASE, TASK_ROLE.BLEND]
                for type in types:
                    comp_sets.append(
                        (
                            self.comp_active_map,
                            f"{TASK_ROLE.LOCATOR}_{type}",
                            f"{TASK_ROLE.DISTANCE}_{type}",
                            loc_position,
                            guide.orientation,
                            "",
                        )
                    )

                # Add attributes for soft, stretch, pin, slide
                attrs = {
                    TASK_ROLE.SOFT: [0.0001, 100, 0.0001],
                    TASK_ROLE.STRETCH: [0.0, 1.0, 0.0],
                    TASK_ROLE.PIN: [0.0, 1.0, 0.0],
                    TASK_ROLE.SLIDE: [-1.0, 1.0, 0.0],
                }
                for attr, (min_val, max_val, default_val) in attrs.items():
                    if not cmds.attributeQuery(attr, node=ik_manipulator.ctrl, exists=True):
                        cmds.addAttr(
                            ik_manipulator.ctrl,
                            ln=attr,
                            at="double",
                            dv=default_val,
                            keyable=True,
                            min=min_val,
                            max=max_val,
                        )

            for comp_map, loc_key, dist_key, pos, rot, flow in comp_sets:
                loc_name = self.format.name(guide.name_raw, item=loc_key, properties=flow)
                dist_name = self.format.name(guide.name_raw, item=dist_key, properties=flow)
                loc, dist = self._create_loc_and_dist(loc_name, dist_name, pos, rot, ik_grp_loc, ik_grp_dist)

                # Map locators and distances
                comp_map.setdefault(guide.name, {})
                comp_map[guide.name][loc_key] = loc
                comp_map[guide.name][dist_key] = dist

        # Step 4 : Parent locators to destignated parent
        active2 = self.active_comps[self.guides[2].name]

        # Parent active end locator to a link group
        active2_loc_grp = cmds.group(n=f"{active2[TASK_ROLE.LOCATOR]}_{TASK_ROLE.LINK}", em=True)
        cmds.xform(active2_loc_grp, ws=True, t=self.guides[2].position, ro=self.guides[2].orientation)
        cmds.parent(active2[TASK_ROLE.LOCATOR], active2_loc_grp)

        # Step 5 : Create IK handle
        ik_handle_name = self.format.name(guide.name_raw)
        ik_solver_name = self.format.name(guide.name_raw, item="RPsolver")
        self.handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=self.joints[0],
            ee=self.joints[2],
            sol="ikRPsolver",
        )[0]

        cmds.rename("effector1", ik_solver_name)
        cmds.setAttr("ikRPsolver.tolerance", 1e-007)
        cmds.parent(self.handle, self.controls[2].ctrl)
        cmds.poleVectorConstraint(self.controls[1].ctrl, self.handle)
