from maya import cmds
from typing import List, Dict, Type, TypeVar, Generic, cast
from core.constant.orbital.format import DIG_Format
from core.constant.orbital import ghost as orbital_ghost


class Node(str):
    """
    Base class for Maya DG nodes.

    This class represents a Maya dependency graph (DG) node. It behaves like a
    string (the node's name) while also storing metadata (side, labels, attributes).

    🚨 This class is NOT intended to be used directly 🚨
       Always subclass it and define `node_type`.

    Subclass contract:
        - Define `node_type` as a class attribute (string).
        - Optionally, extend `__init__` to add shortcut attributes
          (e.g., .input1, .output).

    Example:
        class MultDoubleLinear(Node):
            node_type = "multDoubleLinear"
    """

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
    Base class for sets of nodes.

    This class represents a list of nodes of a specific type.
    🚨 This class is NOT intended to be used directly 🚨
        It is meant to subclass and produce sets of any Node.

    Example:
        class MultDoubleLinearSet(NodeSet[MultDoubleLinear]): ...

    Implementation details:
        - Uses `__orig_bases__` to recover the type argument (`T`) at runtime.
        - The result is stored in `node_class`, which allows NodeSet to
          instantiate the correct node type without subclasses needing to pass it.

    Why `cast`?
        `__orig_bases__` is dynamic and type checkers can't infer its type.
        We use `cast(Type[T], ...)` so that editors (VSCode, PyCharm, mypy)
        know `node_class` really is a subclass of Node. This enables autocomplete
        (e.g., .base_name, .input1) on instances inside the NodeSet.

    Subclass contract:
        - Subclass NodeSet with a concrete Node type, e.g. `NodeSet[MyNode]`.
        - Do not override __init__ unless you need extra logic.
    """

    def __init__(self, base_names: List, side: str, labels: List, attrs_set: List[Dict] = None):
        node_class = cast(Type[T], self.__class__.__orig_bases__[0].__args__[0])

        attrs_set = attrs_set or [{} for _ in base_names]
        for i, (base_name, attrs) in enumerate(zip(base_names, attrs_set)):
            labels_resolved = labels.copy()
            if orbital_ghost.INDEX in labels:
                labels_resolved.remove(orbital_ghost.INDEX)
                labels_resolved.append(f"{i+1:02d}")
            node = node_class(base_name, side, labels_resolved, attrs)
            self.append(node)

    def run(self):
        for node in self:
            node.run()
