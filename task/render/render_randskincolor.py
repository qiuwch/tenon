import sys 
sys.path.append('.')
sys.path.append('../..')
import tenon
import tenon.util
import os

from l23 import L23Job

def main():
    timestamp = tenon.util.shorttimestamp()
    logfile = '/q/cache/tenon/log/render_ranskin_%s.log' % timestamp
    tenon.util.startlogging(logfile)

    l23_randskincolor = L23Job()
    l23_randskincolor.bg = 'off'
    l23_randskincolor.shirtFolder = '//textures/shirt'
    l23_randskincolor.pantsFolder = '//textures/pants'
    l23_randskincolor.skinFolder = '//textures/randSkinColor'

    l23_randskincolor.comment = 'L23 dataset with random skin color'
    l23_randskincolor.outputFolder = '/q/cache/tenon/rendered/randskincolor_%s' % timestamp
    if not os.path.isdir(l23_randskincolor.outputFolder): # Avoid overwrite
        l23_randskincolor.run()

if __name__ == '__main__':
    main()
