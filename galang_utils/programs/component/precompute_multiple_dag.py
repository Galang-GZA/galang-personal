from typing import List
from core.constant.orbital import ghost as orbital_ghost
from core.component.dag import Node


def run(
    Class: Node,
    base_names: List,
    side: str,
    labels: List,
    positions: List[List[float]],
    orientations: List[List[float]],
):
    dags: List = None
    for i, (base_name, position, orientation) in enumerate(zip(base_names, positions, orientations)):
        i = f"{i+1:02d}"
        resolved_labels = [(i if label is orbital_ghost.INDEX else label) for label in labels]
        locator_node = Class(base_name, side, resolved_labels, position, orientation)
        dags.append(locator_node)

    return dags
