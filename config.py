# Include the directory of this script, to make it usable as a package.
import sys
import imp
PWD = '/Users/qiuwch/Dropbox/Workspace/research/CG/'
INRIA_DIR = '/q/cache/dataset/INRIA/'
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
JOINT_FILENAME = RENDER_OUTPUT_DIR + '/joint-PC.csv' # person centric annotation

sys.path.append(PWD)
def r(v):
    imp.reload(v)

# import tenon.demo 
# Do not import this, so that this file can be imported by others

