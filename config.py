# Include the directory of this script, to make it usable as a package.
import sys
import imp

PWD = '/Users/qiuwch/Dropbox/Workspace/research/CG/'
INRIA_DIR = '/q/cache/dataset/INRIA/'
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
JOINT_FILENAME = RENDER_OUTPUT_DIR + '/joint-PC.csv' # person centric annotation

selectedBones = [
	# 1. name of the bone
	# 2. use tail or head location of the bone
    ('shin.fk.L', 'head'),
    ('shin.fk.R', 'head'),
    ('thigh.fk.L', 'head'),
    ('thigh.fk.R', 'head'),
    ('head', 'tail'),
    ('foot.fk.L', 'head'),
    ('foot.fk.R', 'head'),
    ('hand.fk.L', 'head'),
    ('hand.fk.R', 'head'),
    ('forearm.fk.R', 'head'),
    ('forearm.fk.L', 'head'),
    ('upper_arm.fk.L', 'head'),
    ('upper_arm.fk.R', 'head'),
    ('neck', 'head')
]

sys.path.append(PWD)
def r(v):
    imp.reload(v)

# import tenon.demo 
# Do not import this, so that this file can be imported by others

