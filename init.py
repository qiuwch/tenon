# Script to load tenon into blender
import sys
import imp

PWD = '/Users/qiuwch/Dropbox/Workspace/research/CG/'
sys.path.append(PWD)

# Add python site packages into blender, so that I can use third party libs.
# TODO: check python version of blender first
sys.path.append('/usr/local/lib/python3.4/site-packages/')
print(sys.version) # This is the python version. Do not mix python2 and 3 libs.

def r(v):
    imp.reload(v)

# Import for the convinience of interactive shell
import tenon.demo as td
from tenon.render import render
from tenon.config import *
import tenon.pose
import tenon.export
from tenon.bpyutil import *