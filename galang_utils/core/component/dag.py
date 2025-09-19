from maya import cmds
from typing import List
from core.constant.maya.dag import attr as dag_attr
from core.constant.orbital.format import DIG_Format


class Node(str):
    """
    DAG Node is the very base class to create a transfrom node in maya in determined positions.
    This class acts as a string and can be printed, selected, and so on.
    """

    def __new__(cls, base_name: str, side: str, labels: List):
        name_format = DIG_Format(side, base_name, labels).name()
        return super().__new__(cls, name_format)

    def __init__(self, base_name: str, side: str, labels: List, position: List[float], orientation: List[float]):
        # Attributes
        self.translate_x = f"{self}{dag_attr.TRANSLATE_X}"
        self.translate_y = f"{self}{dag_attr.TRANSLATE_Y}"
        self.translate_z = f"{self}{dag_attr.TRANSLATE_Z}"
        self.rotate_x = f"{self}{dag_attr.ROTATE_X}"
        self.rotate_y = f"{self}{dag_attr.ROTATE_Y}"
        self.rotate_z = f"{self}{dag_attr.ROTATE_Z}"
        self.scale_x = f"{self}{dag_attr.SCALE_X}"
        self.scale_y = f"{self}{dag_attr.SCALE_Y}"
        self.scale_z = f"{self}{dag_attr.SCALE_Z}"
        self.visibility = f"{self}{dag_attr.VSIBILITY}"

        # Data
        self.side = side
        self.labels = labels
        self.guide = base_name
        self.position = position
        self.orientation = orientation

    def create_node(self):
        # Creates an empty Maya group at the given position & orientation.
        transform_node = cmds.group(em=True, name=self)
        cmds.xform(transform_node, t=self.position, ro=self.orientation)
