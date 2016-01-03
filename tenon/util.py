import logging
import time
import os

def shorttimestamp():
    timeStamp = time.strftime('%m%d', time.localtime())
    return timeStamp

def longtimestamp():
    timeStamp = time.strftime('%m%d%H%M', time.localtime())
    return timeStamp

def startlogging(logfile, level=logging.DEBUG):
    # The config may be already set by other module, so this would not take effect
    # without removing exsiting handlers

    # Check the log folder, make sure it is writable
    logfolder = os.path.dirname(logfile)
    if not os.path.isdir(logfolder):
        os.mkdir(logfolder)

    for handler in logging.root.handlers[:]: # Reset the existing config
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=logfile,level=logging.DEBUG) 
    logging.info('test message')

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name)
        print('Elapsed: %s' % (time.time() - self.tstart))

class ProgressBar:
    def __init__(self, n, percent=0.05):
        if n == 0:
            print('ProgressBar initialization, n = 0, unexpected case')
        self.n = n
        self.last = 0
        self.percent = percent

    def update(self, i):
        if i == 0:
            print('%d/%d, 0 per, Start... ' % (i, self.n))


        new = float(i) / self.n
        if new - self.last > self.percent:
            print('%d/%d, %.2f per' % (i, self.n, new))
            self.last = new

        if i == (self.n - 1):
            print('%d/%d, 100 per, Finish... ' % (i, self.n))

