"""THIS CONSTANT IS TO BE CHANGED BASED ON THE PROJECT ROLE NEEDS"""

# Project
PROJECT = None  # Project Code
JNT = "jnt"  # Joint
NUM = "001"  # Numbers
IK = "ik"  # Inverse Kinematics
FK = "fk"  # Forward Kinematics
NK = None  # None Kinematics
SUB = None
RESULT = "result"  # Result of IK & FK
BIND = "bind"  # Bind Joint
CTRL = "ctrl"  # Controller
MISC = "misc"  # Miscellaneous
PV = "pv"  # Pole Vector
SCALE = 'scale'
DETAIL = 'detail'
ROLL = 'roll'
SETTINGS = "setings"

# Sides
LEFT = "lt"
RIGHT = "rt"
CENTER = None

# Node Levels
SYSTEM = "system" # Containts all movable objects
DNT = "DNT"  # Do Not Touch Containts all non movable objects
STASIS = "Stasis" # Containts all non movable objects per module
TOP = 'grp'
MASTER = 'grp'
MAIN = "main" # Main Container
GROUP = "grp" # Usually the top node
OFFSET = "offset"
SDK = "sdk"
LINK = "link"
MIRROR = "mirror"
LOCAL = "local"

# Misc DAG
LOCATOR = "loc"
DISTANCE = "dis"

# Nodes
PAIRBLEND = "pairBlend"
SCALEBLEND = "scaleBlend"
REVERSE = "reverse"
PLUS_MIN = "plusplusMinusAverageMinus"
MULT_DIV = "multiplyDivide"
CONDITION = "condition"
BLEND = "blendTwoAttr"
CONSTRAINT = "constraint"

# Node Function
NORMAL = "normalizer"
LEN_ORI = "chainLenOri"
SCALER = "scaler"
ATTR = "attr"
ORI = "ori"
BASE = "base"
SOFT = "soft"
BLEND = "blend"
STRETCH = "stretch"
PIN = "pin"
SLIDE = "slide"
LIMITER = "limiter"

# Node Properties
STATIC = "static"
ACTIVE = "active"
POSITION = 'position'
ORIENT = 'orient'

# Attribute names
FEATURES = "Features"
KINEMATICS = "Kinematic"
IKFKSWITCH = "IkFkSwitch"