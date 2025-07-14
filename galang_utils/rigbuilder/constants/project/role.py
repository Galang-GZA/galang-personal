"""THIS CONSTANT IS TO BE CHANGED BASED ON THE PROJECT ROLE NEEDS"""
class ProjectRole:
    def __init__(self):
        # Project
        self.PROJECT = None  # Project Code
        self.JNT = "jnt"  # Joint
        self.NUM = "001"  # Numbers
        self.IK = "ik"  # Inverse Kinematics
        self.FK = "fk"  # Forward Kinematics
        self.NK = None  # None Kinematics
        self.RESULT = "result"  # Result of IK & FK
        self.BIND = "bind"  # Bind Joint
        self.CTRL = "ctrl"  # Controller
        self.MISC = "misc"  # Miscellaneous
        self.PV = "pv"  # Pole Vector
        
        # Sides
        self.LEFT = "lt"
        self.RIGHT = "rt"
        self.CENTER = None

        # Node Levels
        self.SYSTEM = "system" # Containts all movable objects
        self.DNT = "DNT"  # Do Not Touch Containts all non movable objects
        self.STASIS = "Stasis" # Containts all non movable objects per module
        self.MAIN = "main" # Main Container
        self.GROUP = "grp" # Usually the top node
        self.OFFSET = "offset"
        self.SDK = "sdk"
        self.LINK = "link"
        self.MIRROR = "mirror"
        self.LOCAL = "local"

        # Misc DAG
        self.LOCATOR = "loc"
        self.DISTANCE = "dis"

        # Nodes
        self.PAIRBLEND = "PB"
        self.SCALEBLEND = "SB"
        self.REVERSE = "REV"
        self.PLUS_MINUS = "PM"
        self.MULT_DIV = "MD"
        self.CONDITION = "Cond"
        self.BLEND = "Blend"
        self.CONSTRAINT = "Constraint"

        # Node Function
        self.NORMAL = "Normalizer"
        self.LEN_ORI = "ChainLenOri"
        self.SCALER = "Scaler"
        self.ATTR = "Attr"
        self.ORI = "Ori"
        self.BASE = "Base"
        self.SOFT = "Soft"
        self.BLEND = "Blend"
        self.STRETCH = "Stretch"
        self.PIN = "Pin"
        self.SLIDE = "Slide"
        self.LIMITER = "Limiter"

        # Node Properties
        self.STATIC = "Static"
        self.ACTIVE = "Active"


        # Attribute names
        self.FEATURES = "Features"
        self.KINEMATICS = "Kinematic"
        self.IKFKSWITCH = "IkFkSwitch"