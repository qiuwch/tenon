import logging
import time

def shorttimestamp():
    timeStamp = time.strftime('%m%d', time.localtime())
    return timeStamp

def longtimestamp():
    timeStamp = time.strftime('%m%d%H%M', time.localtime())
    return timeStamp

def startlogging(logfile, level=logging.DEBUG):
    # The config may be already set by other module, so this would not take effect
    # without removing exsiting handlers
    for handler in logging.root.handlers[:]: # Reset the existing config
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=logfile,level=logging.DEBUG) 
    logging.info('test message')
