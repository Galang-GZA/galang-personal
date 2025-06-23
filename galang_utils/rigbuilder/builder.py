"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *
from galang_utils.rigbuilder.modules.module_limb.operator.zoperator import *


class ModuleAssembly:
    def __init__(self, guide):
        self.module_map: Dict = {}
        self.component_map = {LIMB: LimbComponent}
        self.operator_map = {LIMB: LimbOperator}
        self.get_properties(guide)

    def get_properties(self, guide: str) -> None:

        def recursive_get_data(guide):

            # Map the guide module with contents
            module = ModuleInfo(guide)
            self.module_map[str(guide)] = {PROPERTIES: module}

            # Recursive get modules for the child guides
            if module.child:
                for next_guide in module.child:
                    recursive_get_data(next_guide)

        recursive_get_data(guide)

    def build_component(self):

        for module_name, data in self.module_map.items():
            module: ModuleInfo = data[PROPERTIES]
            module_type = module.type
            print("")
            print(f"    Building module: {module_name}, type: {module_type}")

            # Check if component exist for the module type
            ComponentClass = self.component_map.get(module_type)

            if not ComponentClass:
                print(f"    Skipping module {module_name} - no component or operator defined for type {module_type}")
                continue

            # Build the components
            component = ComponentClass(module_name)
            component.create_bind()
            component.create_fk()
            component.create_ik()
            component.create_result()
            component.create_setting()

            # Map the components
            data[COMPONENT] = component

    def run_operator(self):
        for module_name, data in self.module_map.items():
            module: ModuleInfo = data[PROPERTIES]
            module_type = module.type
            print(f"")
            print(f"    Running operators for module: {module_name}, type: {module_type}")

            OperatorClass = self.operator_map.get(module_type)
            component = data.get(COMPONENT)

            if not OperatorClass or not component:
                print(f"    Skipping module {module_name} - missing operator or component for type {module_type}")
                continue

            operator = OperatorClass(component)
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
