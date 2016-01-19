''' 
Provide logging information for error and warning 
Use python logging library
Write logging to files, because the output of blender is too verbose
If want to change to logfile, must change tenon setting, before using this module
In this logging system, I want to seperate the message from tenon library and my specific task code.
'''
import tenon.setting
import logging as L

# format='%(asctime)s %(message)s', datefmt='%Y%m%d-%H%M%S')
# Learn from logging cookbook
logger = L.getLogger('tenon')
logger.propagate = False # Do not contaminate the log of invoking program
logger.setLevel(L.DEBUG)

logfile = tenon.setting.logfile
error_fh = L.FileHandler(logfile.error, delay=True, mode='w')
error_fh.setLevel(L.ERROR) # Can not use setLevel here
info_fh = L.FileHandler(logfile.info, delay=True, mode='w')
info_fh.setLevel(L.INFO)
warning_fh = L.FileHandler(logfile.warning, delay=True, mode='w')
warning_fh.setLevel(L.WARNING)
debug_fh = L.FileHandler(logfile.debug, delay=True, mode='w')
debug_fh.setLevel(L.DEBUG)

formatter = L.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

for v in [error_fh, info_fh, warning_fh, debug_fh]:
    v.setFormatter(formatter)
    logger.addHandler(v)

info = logger.info
error = logger.error
debug = logger.debug
warning = logger.warning

# TODO: fix bug of this logging module later.