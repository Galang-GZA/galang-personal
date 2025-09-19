from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class MultDoubleLinear(Node):
    """
    Represents a Maya multDoubleLinear node.

    Subclass of Node that defines `node_type` and adds
    convenient properties for inputs/outputs.
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
    Represents a list of multDoubleLinear nodes.

    Subclass of NodeSet bound to MultDoubleLinear.
    Automatically creates multiple nodes with indexed labels if required.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(base_names, side, labels, attrs_set)
