# Include the directory of this script, to make it usable as a package.
import sys
import imp

PWD = '/Users/qiuwch/Dropbox/Workspace/research/CG/'
sys.path.append(PWD)
def r(v):
    imp.reload(v)

import tenon.demo 

