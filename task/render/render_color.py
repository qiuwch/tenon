import sys 
sys.path.append('.')
sys.path.append('..')
import tenon
import tenon.util
import os

from l23 import L23Job

def main():
    timestamp = tenon.util.shorttimestamp()
    logfile = '%s/render_color_%s.log' % (os.getcwd(), timestamp)
    tenon.util.startlogging(logfile)

    # l23_color_cloth = L23Job('l23color')
    l23_color_cloth = L23Job()
    l23_color_cloth.cloth = 'color'
    l23_color_cloth.comment = 'L23 dataset with pure color cloth'
    l23_color_cloth.outputFolder = './no_bg/'
    l23_color_cloth.run()

if __name__ == '__main__':
    main()
