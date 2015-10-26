import glob
# Define global variables for this project.
INRIA_DIR = '//background/INRIA/'
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
TMP_DIR = '/q/cache/'
JOINT_FILENAME = RENDER_OUTPUT_DIR + '/joint-PC.csv' # person centric annotation
lspJointFile = '/q/cache/lsp_2d_3d/joint_3d/2015101415_v2/%04d.csv' # This is unnormalized version

# human_model = 'human_model'
# human_model = 'man_in_short'

selectedBones = [
	# 1. name of the bone
	# 2. use tail or head location of the bone
    ('thigh.fk.L', 'tail'), # ('shin.fk.L', 'head'),
    ('thigh.fk.R', 'tail'), # easier for rotation
    ('thigh.fk.L', 'head'),
    ('thigh.fk.R', 'head'),
    ('head', 'tail'),
    ('shin.fk.L', 'tail'), # ('foot.fk.L', 'head'),
    ('shin.fk.R', 'tail'), # ('foot.fk.R', 'head'),
    ('forearm.fk.L', 'tail'), #('hand.fk.L', 'head'),
    ('forearm.fk.R', 'tail'), # ('hand.fk.R', 'head'),
    ('upper_arm.fk.L', 'tail'), # ('forearm.fk.R', 'head'),
    ('upper_arm.fk.R', 'tail'), # ('forearm.fk.L', 'head'),
    ('upper_arm.fk.L', 'head'),
    ('upper_arm.fk.R', 'head'),
    ('neck', 'head')
]

# This is moved to puppet.py
# Define the skeleton
connections = [
    # Leg
    ('thigh.fk.L.head', 'thigh.fk.L.tail'),
    ('thigh.fk.R.head', 'thigh.fk.R.tail'),
    ('thigh.fk.L.tail', 'shin.fk.L.tail'),
    ('thigh.fk.R.tail', 'shin.fk.R.tail'),
    # Arm
    ('upper_arm.fk.L.head', 'upper_arm.fk.L.tail'),
    ('upper_arm.fk.R.head', 'upper_arm.fk.R.tail'),
    ('upper_arm.fk.L.tail', 'forearm.fk.L.tail'),
    ('upper_arm.fk.R.tail', 'forearm.fk.R.tail'),
    # Head
    ('head.tail', 'neck.head'),
    ('thigh.fk.L.head', 'upper_arm.fk.L.head'),
    ('thigh.fk.R.head', 'upper_arm.fk.R.head')
]

def bpyPathHelper(relpath):
    # Convert blender relpath to something accessible to other code
    try:
        import bpy
        path = bpy.path.abspath(relpath)
    except:
        path = relpath.replace('//', '../scenes/')
    return path
    
