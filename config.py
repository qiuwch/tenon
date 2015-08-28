# Include the directory of this script, to make it usable as a package.
import sys
import imp
PWD = '/Users/qiuwch/Dropbox/Workspace/research/'
INRIA_DIR = '/q/data/INRIA/'
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
sys.path.append(PWD)
def r(v):
    imp.reload(v)

import tenon.demo

