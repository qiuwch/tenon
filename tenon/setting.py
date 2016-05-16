# Configuration of tenon
# from tenon.util import timestamp, dictwrapper

import sys, os
sys.path.append(os.path.expanduser('~'))

blender = 'blender'

try:
    from local_settings import *
except:
    pass
