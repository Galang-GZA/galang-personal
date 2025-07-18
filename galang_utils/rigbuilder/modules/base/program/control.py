from maya import cmds
from typing import Dict
from galang_utils.curve import shapes_library as gen_shapes
from galang_utils.rigbuilder.constant.general import role as GEN_ROLE
from galang_utils.rigbuilder.constant.general import setup as GEN_SETUP
from galang_utils.rigbuilder.constant.project import role as TASK_ROLE
from galang_utils.rigbuilder.constant.project import setup as task_setup
from galang_utils.rigbuilder.modules.base.constant.format import BaseFormat 
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo


class BaseControlCreator:
    def __init__(self, guide: GuideInfo, kinematics, module: ModuleInfo):
        self.guide = guide
        self.module = module
        self.kinematics = kinematics
        self.ctrl = None
        self.top = None
        self.nodes:Dict = {}
        self.format = BaseFormat(self.kinematics, self.guide.side)

        # Node level flags to be passed on later if needed
        self.node_flags = {level: task_setup.NODE_DEFAULT_FLAGS.get(level, False) for level in task_setup.NODE_MAIN_LEVELS}

    def get_node(self, level):

        # Returns the transform node for the given node level (e.g., 'offset', 'sdk')
        return self.nodes.get(level)

    def create(self, color_set: Dict = task_setup.MAIN_COLOR, node_level=task_setup.NODE_MAIN_LEVELS, local=None):
        # Creates a cpmtrp; curve with the appropriate level hierarchy and mirror transform if needed.
        if self.guide.side_id == None or self.guide.position is None or self.guide.orientation is None:
            cmds.warning(f"Cannot creat control for this guide:{self.guide.name_raw} lha~")
            return

        # Create control based on the shapes library or basic shapes
        if TASK_ROLE.PV in self.guide.name:
            shape_type = GEN_ROLE.HINGES
        else:
            shape_type = self.module.type
        shape_data = gen_shapes.SHAPES_LIBRARY.get(self.kinematics, {}).get(shape_type)

        if shape_data:
            self.ctrl = cmds.curve(
                d=shape_data["degree"],
                p=shape_data["control_points"],
                name=self.format.name(self.guide.name_raw, TASK_ROLE.CTRL),
            )
            cmds.xform(self.ctrl, s=(self.guide.size, self.guide.size, self.guide.size))
            cmds.makeIdentity(self.ctrl, a=True, t=1, r=1, s=1)
            self.nodes[TASK_ROLE.CTRL] = self.ctrl
        else:
            circle_normal = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}
            # print(f"Defaulting {self.guide.name} to circle")
            self.ctrl = cmds.circle(
                n=self.format.name(self.guide.name_raw, TASK_ROLE.CTRL),
                normal=circle_normal.get(self.module.axis),
                ch=False,
                radius=self.guide.size,
            )[0]
            self.nodes[TASK_ROLE.CTRL] = self.ctrl
        attrs = ["visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

        # Apply color to the control
        shape = cmds.listRelatives(self.ctrl, shapes=True)[0]
        color_id = color_set.get(self.guide.side_id, task_setup.COLOR_INDEX["yellow"])
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        cmds.setAttr(f"{shape}.overrideColor", color_id)

        # Building controls level hieararchy based on NODE_LEVELS
        top_node = self.ctrl
        for level in node_level:
            cmds.select(clear=True)
            if self.node_flags[level]:
                node = cmds.group(
                    em=True,
                    name=self.format.name(self.guide.name_raw, TASK_ROLE.CTRL, level=level),
                    
                )
                if self.guide.side_id == task_setup.MIRROR_SIDE_ID and level == TASK_ROLE.MIRROR:
                    mirror_data = GEN_SETUP.MIRROR_AXIS_DATA[task_setup.MIRROR_AXIS]
                    cmds.xform(
                        node,
                        ro=mirror_data["orientation"],
                        s=mirror_data["scale"],
                    )
                cmds.parent(top_node, node)  # Parent lower node under this one
                if self.guide.side_id == task_setup.MIRROR_SIDE_ID and level == TASK_ROLE.MIRROR:
                    cmds.xform(top_node, ro=(0, 180, 0))
                    cmds.makeIdentity(top_node, a=True, t=1, r=1, s=1)  # Freeze transform node bellow MIRROR
                self.nodes[level] = node
                top_node = node

        cmds.xform(top_node, ws=True, t=self.guide.position, ro=self.guide.orientation)
        self.top = top_node  # Topmost node for parenting
