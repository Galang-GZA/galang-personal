from maya import cmds
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat 


class NodeCreator:
    def __init__(self, side, kinematics=None):
        self.format = LimbFormat(side, kinematics)
    
    def setup(self, guide_name_raw=None, type=None, properties1=None, properties2=None, attr1=None, value1=None, attr2=None, value2=None, attr3=None, value3=None, i=None):
        # Create Node
        node = cmds.createNode(type, n=self.format.name(guide_name_raw, type, properties1, properties2, attr1, value1, attr2, value2, attr3, value3, i))
        
        # Set attributes
        if attr1 and value1:
            cmds.setAttr(f'{node}.{attr1}', value1)
        if attr2 and value2:
            cmds.setAttr(f'{node}.{attr2}', value2)
        if attr3 and value3:
            cmds.setAttr(f'{node}.{attr3}', value3)

        return node