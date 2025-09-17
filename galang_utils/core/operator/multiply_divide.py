from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class MultiplyDivide(Node):
    """
    MultiplyDivide creates a multiplyDivide node in maya.
    This class acts as a string and can be printed, selected, and so on.
    This class subclasses DG Node but doesnt strict the full_type to have a node type in it.
    Node type will be handled by this class.
    """

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        super().__init__(base_name, side, labels, dg_role.MULT_DIV, attrs)

        # Input Attributes
        self.input1X = f"{self}{dg_attr.INPUT1_X}"
        self.input1Y = f"{self}{dg_attr.INPUT1_Y}"
        self.input1Z = f"{self}{dg_attr.INPUT1_Z}"
        self.input2X = f"{self}{dg_attr.INPUT2_X}"
        self.input2Y = f"{self}{dg_attr.INPUT2_Y}"
        self.input2Z = f"{self}{dg_attr.INPUT2_Z}"

        # Output Attributes
        self.outputX = f"{self}{dg_attr.OUTPUT_X}"
        self.outputY = f"{self}{dg_attr.OUTPUT_Y}"
        self.outputZ = f"{self}{dg_attr.OUTPUT_Z}"

        # Misc Attributes
        self.operation = f"{self}{dg_attr.OPERATION}"


class MultiplyDivideSet(NodeSet):
    """
    DistanceSet creates a set of multiplyDivide nodes in maya.
    This class acts as a list and can be printed, for loop selected, and so on.
    This class subclasses DG NodeSet, instancing MultiplyDivide class in super __init__.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(MultiplyDivide, base_names, side, labels, dg_role.MULT_DIV, attrs_set)
