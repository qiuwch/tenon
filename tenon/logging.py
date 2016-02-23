'''
Provide logging information for error and warning
Use python logging library
Write logging to files, because the output of blender is too verbose
If want to change to logfile, must change tenon setting, before using this module
In this logging system, I want to seperate the message from tenon library and my specific task code.
'''
import tenon.setting
import logging as L
import sys

# format='%(asctime)s %(message)s', datefmt='%Y%m%d-%H%M%S')
# Learn from logging cookbook
logger = L.getLogger('tenon')
logger.propagate = False # Do not contaminate the log of invoking program
# logger.setLevel(L.DEBUG)
logger.setLevel(L.INFO) # Default level should be INFO

logfilename = tenon.setting.logfile
error_fh = L.FileHandler(logfilename.error, delay=True, mode='w')
error_fh.setLevel(L.ERROR) # Can not use setLevel here
info_fh = L.FileHandler(logfilename.info, delay=True, mode='w')
info_fh.setLevel(L.INFO)
warning_fh = L.FileHandler(logfilename.warning, delay=True, mode='w')
warning_fh.setLevel(L.WARNING)
debug_fh = L.FileHandler(logfilename.debug, delay=True, mode='w')
debug_fh.setLevel(L.DEBUG)

sh = L.StreamHandler(sys.stderr)
sh.setLevel = (L.DEBUG)

formatter = L.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# for v in [error_fh, info_fh, warning_fh, debug_fh, sh]:
for v in [debug_fh, sh]:
    v.setFormatter(formatter)
    logger.addHandler(v)

info = logger.info
error = logger.error
debug = logger.debug
warning = logger.warning

DEBUG = L.DEBUG
INFO = L.INFO
WARNING = L.WARNING
ERROR = L.ERROR

def setLevel(level):
    logger.setLevel(level)

# TODO: fix bug of this logging module later.
