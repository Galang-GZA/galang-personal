from typing import List, Dict
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.operator.dg import Node, NodeSet


class MultiplyDivide(Node):
    """
    Represents a Maya multiplyDivide node.

    Subclass of Node that defines `node_type` and adds
    convenient properties for inputs/outputs/operation.
    """

    node_type = dg_role.MULT_DIV

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        super().__init__(base_name, side, labels, attrs)

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


class MultiplyDivideSet(NodeSet[MultiplyDivide]):
    """
    Represents a list of multiplyDivide nodes.

    Subclass of NodeSet bound to MultiplyDivide.
    Automatically creates multiple nodes with indexed labels if required.
    """

    def __init__(self, base_names: List, side, labels: List, attrs_set: List[Dict] = None):
        super().__init__(base_names, side, labels, attrs_set)
