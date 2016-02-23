# Configuration of tenon
from tenon.util import timestamp, dictwrapper

import sys, os
sys.path.append(os.path.expanduser('~'))

blender = '/Applications/blender.app/Contents/MacOS/blender'
loglevel = dictwrapper(debug=False, warning=True, error=True, info=True)
_default_log_file = 'tenon-%s.log' % timestamp()
logfile = dictwrapper(debug = _default_log_file,
    info = _default_log_file,
    warning = 'tenon-warning-%s.log' % timestamp(),
    error = 'tenon-error-%s.log' % timestamp())

from local_settings import *
