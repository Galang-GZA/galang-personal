"""Create Hand Rig Based On the Guide Joints"""

from typing import Dict
from galang_utils.rigbuilder.constant.general import role as gen_role
from galang_utils.rigbuilder.core.guide import ModuleInfo
from rigbuilder.modules.base.component.z_component import BaseComponent
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent
from galang_utils.rigbuilder.modules.limb.operator.zoperator import LimbOperator


class ModuleAssembly:
    def __init__(self, guide):
        self.module_map: Dict = {}
        self.get_properties(guide)

    def get_properties(self, guide: str) -> None:

        def recursive_get_data(guide):
            # Map the guide module with contents
            module = ModuleInfo(guide)

            if module.type == gen_role.LIMB:
                component = LimbComponent(module)
                operator = LimbOperator(module)
                self.module_map[str(guide)] = {gen_role.COMPONENT: component, gen_role.OPERATOR: operator}
            # elif module.type == HAND:
            #     component = HandComponent(module)
            #     operator = HandOperator(component)
            #     self.module_map[str(guide)] = {COMPONENT: component, OPERATOR: operator}
            # elif module.type == FINGER:
            #     component = FingerComponent(module)
            #     operator = FingerOperator(component)
            #     self.module_map[str(guide)] = {COMPONENT: component, OPERATOR: operator}
            # elif module.type == SPINE:
            #     component = SpineComponent(module)
            #     operator = SpineOperator(component)
            #     self.module_map[str(guide)] = {COMPONENT: component, OPERATOR: operator}

            # Recursive get modules for the child guides
            if module.child:
                for next_guide in module.child:
                    recursive_get_data(next_guide)

        recursive_get_data(guide)

    def build_component(self):

        for module_name, data in self.module_map.items():
            component: BaseComponent = data[gen_role.COMPONENT]

            if component:
                print(f"    Building module: {module_name}")
            else:
                print(f"    Skipping module {module_name}")
                continue

            # Build the components
            component.create_bind()
            component.create_rig()

    def run_operator(self):
        for module_name, data in self.module_map.items():
            component: BaseComponent = data[gen_role.COMPONENT]
            operator = LimbOperator(component)  # PR UBAH JADIIN BASE OPERATOR
            data[gen_role.OPERATOR] = operator
            if operator or component:
                print(f"    Running module: {module_name}")
            else:
                print(f"    Skipping module {module_name}")
                continue

            operator.run_bind()
            operator.run()

    # Debugging procedures
    def __repr__(self):
        lines = ["<ModuleAssembly>"]
        for guide_name in self.module_map:
            module = ModuleInfo(guide_name)

            lines.append(f"    Module         : {guide_name}, (type = {module.type}, axis = {module.axis})")
            lines.append(f"    Guides         : {[g.name for g in module.guides]}")
            lines.append(f"    Guides End     : {[g.name for g in module.guides_end]}")
            lines.append(f"    Guides PV      : {[g.name for g in module.guides_pv]}")
            lines.append(f"    Parent Module  : {module.parent}")
            lines.append(f"    Child Modules  : {module.child}")
            lines.append("")

        return "\n".join(lines)
