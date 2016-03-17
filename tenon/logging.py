'''
Provide logging information for error and warning
Use python logging library
Write logging to files, because the output of blender is too verbose
If want to change to logfile, must change tenon setting, before using this module
In this logging system, I want to seperate the message from tenon library and my specific task code.
'''
from __future__ import absolute_import
import logging # This is the system logging module
import sys

# No dependency on other modules, this is a core module and needs to be very stable
# from tenon.util import timestamp, dictwrapper

def prettify_filename(filename):
    '''
    Make the filename in the console clickable
    '''
    import os
    from sys import platform as _platform
    filename = os.path.expanduser(filename)
    filename = os.path.abspath(filename)

    if _platform == "linux" or _platform == "linux2":
        filename = 'file://%s' % filename

    return filename

def time_stamp():
    import datetime
    n = datetime.datetime.now()
    return n.strftime('%Y%m%d-%H%M%S')

default_log_file = 'tenon-%s.log' % time_stamp()

# Learn from logging cookbook
logger = logging.getLogger('tenon')
logger.propagate = False # Do not contaminate the log of invoking program

# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO) # Default level should be INFO

fh = logging.FileHandler(default_log_file, delay = True, mode='w')
fh.setLevel(logging.ERROR)

sh = logging.StreamHandler(sys.stderr)
sh.setLevel = (logging.DEBUG)

# format='%(asctime)s %(message)s', datefmt='%Y%m%d-%H%M%S')
format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(format)

for v in [sh, fh]:
    v.setFormatter(formatter)
    logger.addHandler(v)

info = logger.info
error = logger.error
debug = logger.debug
warning = logger.warning

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

def setLevel(level):
    logger.setLevel(level)

def fileLevel(level):
    '''
    Which level should be save to a log file
    Default is None
    '''
    fh.setLevel(level)

def isDebug():
    return logger.level == logging.DEBUG
# TODO: fix bug of this logging module later.

