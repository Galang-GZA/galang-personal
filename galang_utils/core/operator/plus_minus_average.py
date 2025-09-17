from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class PlusMinusAverage(Node):
    """
    PlusMinusAverage creates a plusMinusAverage node in maya.
    This class acts as a string and can be printed, selected, and so on.
    This class subclasses DG Node but doesnt strict the full_type to have a node type in it.
    Node type will be handled by this class.
    """

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        super().__init__(base_name, side, labels, attrs, dg_role.PLUS_MIN, attrs)

        # Input Attributes
        self.input1D0 = f"{self}{dg_attr.INPUT_1D0}"
        self.input1D1 = f"{self}{dg_attr.INPUT_1D1}"
        self.input1D2 = f"{self}{dg_attr.INPUT_1D2}"

        # Output Attribute
        self.output1D = f"{self}{dg_attr.OUTPUT_1D}"

        # Misc Attribute
        self.operation = f"{self}{dg_attr.OPERATION}"


class MultDoubleLinearSet(NodeSet):
    """
    MultDoubleLinearSet creates a set of plusMinusAverage nodes in maya.
    This class acts as a list and can be printed, for loop selected, and so on.
    This class subclasses DG NodeSet, instancing PlusMinusAverage class in super __init__.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(PlusMinusAverage, base_names, side, labels, dg_role.PLUS_MIN, attrs_set)
