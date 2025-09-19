from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class PlusMinusAverage(Node):
    """
    Represents a Maya plusMinusAverage node.

    Subclass of Node that defines `node_type` and adds
    convenient properties for inputs/outputs.
    """

    node_type = dg_role.PLUS_MIN

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        super().__init__(base_name, side, labels, attrs, attrs)

        # Input Attributes
        self.input1D0 = f"{self}{dg_attr.INPUT_1D0}"
        self.input1D1 = f"{self}{dg_attr.INPUT_1D1}"
        self.input1D2 = f"{self}{dg_attr.INPUT_1D2}"

        # Output Attribute
        self.output1D = f"{self}{dg_attr.OUTPUT_1D}"

        # Misc Attribute
        self.operation = f"{self}{dg_attr.OPERATION}"


class MultDoubleLinearSet(NodeSet[PlusMinusAverage]):
    """
    Represents a list of plusMinusAverage nodes.

    Subclass of NodeSet bound to PlusMinusAverage.
    Automatically creates multiple nodes with indexed labels if required.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(base_names, side, labels, attrs_set)
