import sys 
sys.path.append('.')
sys.path.append('..')
import tenon
import tenon.util
import os

from l23 import L23Job

def main():
    timestamp = tenon.util.shorttimestamp()
    logfile = '%s/render_no_bg_%s.log' % (os.getcwd(), timestamp)
    tenon.util.startlogging(logfile)

    l23_texture_cloth = L23Job('l23textureBrodatz')
    l23_texture_cloth.cloth = 'textureBrodatz'
    l23_texture_cloth.comment = 'L23 dataset with Texture pattern as cloth'
    l23_texture_cloth.outputFolder = './texture/'
    l23_texture_cloth.run()

if __name__ == '__main__':
    main()
