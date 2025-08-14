from maya import cmds
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat


class NodeCreator:
    def __init__(self, side, kinematics=None):
        self.format = LimbFormat(side, kinematics)

    def setup(
        self,
        guide_name_raw=None,
        type=None,
        properties1=None,
        properties2=None,
        attr1=None,
        val1=None,
        attr2=None,
        val2=None,
        attr3=None,
        val3=None,
        i=None,
    ):
        # Create Node
        node = cmds.createNode(type, n=self.format.name(guide_name_raw, type, properties1, properties2, i))

        # Set attributes
        if attr1 and val1:
            cmds.setAttr(f"{node}.{attr1}", val1)
        if attr2 and val2:
            cmds.setAttr(f"{node}.{attr2}", val2)
        if attr3 and val3:
            cmds.setAttr(f"{node}.{attr3}", val3)

        return node
