from maya import cmds
from typing import List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.base import LimbBaseNode
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode


class LimbLocatorNode(LimbBaseNode):
    """
    LimbLocatorNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        types: List = None,
        index: int = None,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        # This will add locator string to types if not exsit yet
        # usable for creating locator a la carte
        if not role.LOCATOR in types:
            types.insert(0, role.LOCATOR)

        # pre-compute locator name
        super().__init__(guide, module, kinematics, types, index, position, orientation)

    def create(self):
        """
        Creates an empty Maya group at the given position & orientation.
        """
        loc_node = cmds.spaceLocator(name=self)
        cmds.xform(loc_node, t=self.position, ro=self.orientation)


class LimbLocatorSet(List[LimbLocatorNode]):
    """
    A collection of LimbLocatorSet indexed by their locator index and type (e.g. "STRETCH", "BASE", "BLEND", etc.).
    """

    def __init__(self, module: ModuleInfo, kinematics: str, types: List):
        super().__init__()
        guide = module.guide
        guides = module.guides
        self.group = LimbGroupNode(guide, module, kinematics, types, level=role.GROUP)

        # Pre-compute locators (they’re not yet in Maya)
        # Pre-compute general locators
        loc_types: List = types.insert(0, role.LOCATOR)
        pv_pos = module.guides_pv[0].position
        for i, guide in enumerate(guides):
            if role.ACTIVE in types and i == 1:
                locator_node = LimbLocatorNode(guide, module, kinematics, loc_types, pv_pos)
            else:
                locator_node = LimbLocatorNode(guide, module, kinematics, loc_types)
            self.append(locator_node)

        # Pre-compute soft IK locators
        if role.ACTIVE in types == role.ACTIVE:
            self.stretch = LimbLocatorNode(guides[2], module, kinematics, loc_types.append(role.STRETCH))
            self.base = LimbLocatorNode(guides[2], module, kinematics, loc_types.append(role.BASE))
            self.blend = LimbLocatorNode(guides[2], module, kinematics, loc_types.append(role.BLEND))
            self.active_list: List[LimbLocatorNode] = [self.stretch, self.base, self.blend]

    def create(self):
        # Create group node
        self.group.create()

        # Create guide positioned locators
        for loc in self:
            loc.create()

        # Create soft IK locators
        for extra_loc in self.active_list:
            extra_loc.create()
