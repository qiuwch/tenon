import sys 
sys.path.append('.')
sys.path.append('../..')
import tenon
import tenon.util
import os

from l23 import L23Job

def main():
    timestamp = tenon.util.shorttimestamp()
    logfile = '/q/cache/tenon/log/render_no_bg_%s.log' % timestamp
    tenon.util.startlogging(logfile)

    l23_no_bg = L23Job()
    l23_no_bg.bg = 'off'
    l23_no_bg.shirtFolder = '//textures/randomColor'
    l23_no_bg.pantsFolder = '//textures/randomColor'

    l23_no_bg.comment = 'L23 dataset with pure color cloth'
    l23_no_bg.outputFolder = '/q/cache/tenon/rendered/no_bg_%s' % timestamp
    if not os.path.isdir(l23_no_bg.outputFolder): # Avoid overwrite
        l23_no_bg.run()

if __name__ == '__main__':
    main()
