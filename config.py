# Define global variables for this project.
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
lspJointFile = '/q/cache/lsp_2d_3d/joint_3d/2015101415_v2/%04d.csv' # This is unnormalized version

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

def bpyPathHelper(relpath):
    # Convert blender relpath to something accessible to other code
    try:
        import bpy
        path = bpy.path.abspath(relpath)
    except:
        path = relpath.replace('//', '../scenes/')
    return path
    
