from typing import List
from core.constant.orbital import shell as global_shell


def run(labels: List[str], i: int):
    resolved_labels = labels.copy()
    if global_shell.INDEX in labels:
        resolved_labels.remove(global_shell.INDEX)
        resolved_labels.append(f"{i+1:02d}")

    return resolved_labels
