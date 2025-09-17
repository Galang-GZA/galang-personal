from maya import cmds
from typing import List, Dict, Type, TypeVar, Generic
from core.constant.orbital.format import DIG_Format
from core.constant.orbital import ghost as orbital_ghost


class Node(str):
    """
    DG Node is the very base class to subclass other node creator class
    to create a dg node in maya and set the attributes needed.
    THIS IS NOT A STAND ALONE CLASS. USE FOR SUBCLASSING ONLY.
    """

    # Subclass will always be the one defining its node_type
    node_type: str = None

    def __new__(cls, base_name: str, side: str, labels: List):
        name_format = DIG_Format(side, base_name, labels).name()
        return super().__new__(cls, name_format)

    def __init__(self, base_name: str, side: str, labels: List, attrs: Dict = None):
        # Data
        self.side = side
        self.labels = labels
        self.attributes = attrs
        self.base_name = base_name

    def run(self):
        # Create Node
        node = cmds.createNode(self.node_type, n=self)

        # Set attributes
        if self.attributes:
            for attr, value in self.attributes.items():
                cmds.setAttr(f"{node}.{attr}", value)


# Type variable bound to Node
T = TypeVar("T", bound=Node)


class NodeSet(List[T], Generic[T]):
    """
    DG NodeSet is the very base class to subclass other node set creator class
    to create a set dg nodes in maya and set the attributes needed.
    THIS IS NOT A STAND ALONE CLASS. USE FOR SUBCLASSING ONLY.
    """

    def __init__(self, Node_Class: Type[T], base_names: List, side: str, labels: List, attrs_set: List[Dict] = None):
        attrs_set = attrs_set or [{} for _ in base_names]
        for i, (base_name, attrs) in enumerate(zip(base_names, attrs_set)):
            labels_resolved = labels.copy()
            if orbital_ghost.INDEX in labels:
                labels_resolved.remove(orbital_ghost.INDEX)
                labels_resolved.append(f"{i+1:02d}")
            node = Node_Class(base_name, side, labels_resolved, attrs)
            self.append(node)

    def run(self):
        for node in self:
            node.run()
