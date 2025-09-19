from typing import List, Type, TypeVar
from core.component.dag import Node
from core.support.node import apply_index_to_labels


T = TypeVar("T", bound=Node)


def run(
    Class: Type[T],
    base_names: List,
    side: str,
    labels: List,
    positions: List[List[float]],
    orientations: List[List[float]],
) -> List[T]:
    dags: List[T] = []
    for i, (base_name, position, orientation) in enumerate(zip(base_names, positions, orientations)):
        resolved_labels = apply_index_to_labels.run(labels, i)
        locator_node = Class(base_name, side, resolved_labels, position, orientation)
        dags.append(locator_node)

    return dags
