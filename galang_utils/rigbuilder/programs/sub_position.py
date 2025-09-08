from typing import List
from rigbuilder.cores.guide import ModuleInfo


class SubPositions:
    def __init__(self, module: ModuleInfo, sub_divs: int, i: int):
        self.sub_divs = sub_divs
        self.root_position = module.guides[i].position
        self.end_position = module.guides[i + 1].position
        self.sub_positions: List = None

    def get(self):
        for i in range(self.sub_divs):
            ratio = i / self.sub_divs
            sub_position = [
                self.root_position[n] + ratio * (self.end_position[n] - self.root_position[n]) for n in range(3)
            ]
            self.sub_positions.append(sub_position)
