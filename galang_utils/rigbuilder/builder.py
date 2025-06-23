"""Create Hand Rig Based On the Guide Joints"""

from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import LimbComponent
from galang_utils.rigbuilder.modules.module_limb.operator.zoperator import LimbOperator


class ModuleAssembly:
    def __init__(self, guide):
        self.module_map: Dict = {}
        self.get_properties(guide)

    def get_properties(self, guide: str) -> None:

        def recursive_get_data(guide):
            # Map the guide module with contents
            module = ModuleInfo(guide)
            # if module.type == SPINE:
            #     self.module_map[str(guide)] = {COMPONENT: SpineComponent(module), OPERATOR: SpineOperator(module)}
            if module.type == LIMB:
                self.module_map[str(guide)] = {COMPONENT: LimbComponent(module), OPERATOR: LimbOperator(module)}
            # if module.type == HAND:
            #     self.module_map[str(guide)] = {COMPONENT: HandComponent(module), OPERATOR: HandOperator(module)}
            # if module.type == FINGER:
            #     self.module_map[str(guide)] = {COMPONENT: FingerComponent(module), OPERATOR: FingerOperator(module)}

            # Recursive get modules for the child guides
            if module.child:
                for next_guide in module.child:
                    recursive_get_data(next_guide)

        recursive_get_data(guide)

    def build_component(self):

        for module_name, data in self.module_map.items():
            component: LimbComponent = data[COMPONENT]

            if component:
                print(f"    Building module: {module_name}")
            else:
                print(f"    Skipping module {module_name}")
                continue

            # Build the components
            component.create_bind()
            component.create_fk()
            component.create_ik()
            component.create_result()
            component.create_setting()

    def run_operator(self):
        for module_name, data in self.module_map.items():
            component: LimbComponent = data[COMPONENT]
            operator: LimbOperator = data[OPERATOR]

            if operator or component:
                print(f"    Running operators for module: {module_name}")
            else:
                print(f"    Skipping module {module_name}")
                continue

            operator.run_bind()
            operator.run_fk()
            operator.run_ik()
            operator.run_result()
            operator.run_setting()

    # Debugging procedures
    def __repr__(self):
        lines = ["<ModuleAssembly>"]
        for guide_name, data in self.module_map.items():
            module: ModuleInfo = data[PROPERTIES]

            lines.append(f"    Module         : {guide_name}, (type = {module.type}, axis = {module.axis})")
            lines.append(f"    Guides         : {[g.name for g in module.guides]}")
            lines.append(f"    Guides End     : {[g.name for g in module.guides_end]}")
            lines.append(f"    Guides PV      : {[g.name for g in module.guides_pv]}")
            lines.append(f"    Parent Module  : {module.parent}")
            lines.append(f"    Child Modules  : {module.child}")
            lines.append("")

        return "\n".join(lines)
