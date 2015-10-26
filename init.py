# Script to load tenon into blender
import sys, imp
import bpy

# Space between = is required
PWD = '/q/run/'
sitePkg = '/usr/local/lib/python3.4/site-packages/'

for v in [PWD, sitePkg]:
    sys.path.append(v)

# Add python site packages into blender, so that I can use third party libs.
# TODO: check python version of blender first
print(sys.version) # This is the python version. Do not mix python2 and 3 libs.

def r(v):
    imp.reload(v)

# Setup the logging for this session
import logging
debugFile = bpy.path.abspath('//debug.log')
print('Log is saved to %s' % debugFile)
logging.basicConfig(filename=debugFile,level=logging.DEBUG)
logging.info('Test message.')
# TODO: add timestamp to the filename

import tenon.task
import tenon.puppet as pp
import tenon.scene as sc