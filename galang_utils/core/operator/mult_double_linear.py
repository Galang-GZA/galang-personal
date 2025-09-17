from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class MultDoubleLinear(Node):
    """
    MultDoubleLinear creates a multDoubleLinear node in maya.
    This class acts as a string and can be printed, selected, and so on.
    Node type will be handled by this class.
    """

    node_type = dg_role.MULT_DOUBLE_LINEAR

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        super().__init__(base_name, side, labels, attrs)

        # Input Attributes
        self.input1 = f"{self}{dg_attr.INPUT1}"
        self.input2 = f"{self}{dg_attr.INPUT2}"

        # Output Attributes
        self.output = f"{self}{dg_attr.OUTPUT}"


class MultDoubleLinearSet(NodeSet[MultDoubleLinear]):
    """
    DistanceSet creates a set of multDoubleLinear nodes in maya.
    This class acts as a list and can be printed, for loop selected, and so on.
    This class subclasses DG NodeSet, instancing MultDoubleLinear class in super __init__.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(MultDoubleLinear, base_names, side, labels, attrs_set)
