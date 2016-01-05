import sys 
sys.path.append('.')
sys.path.append('../..')
import tenon
import tenon.util
import os

from l23 import L23Job

def main():
    timestamp = tenon.util.shorttimestamp()
    logfile = '%s/render_texture_%s.log' % (os.getcwd(), timestamp)
    tenon.util.startlogging(logfile)

    l23_texture_cloth = L23Job()
    l23_texture_cloth.shirtFolder = '//textures/ColorBrodatzPng'
    l23_texture_cloth.pantsFolder = '//textures/ColorBrodatzPng'
    l23_texture_cloth.skinFolder = '//textures/randSkinColor'

    l23_texture_cloth.comment = 'L23 dataset with Texture pattern as cloth'
    l23_texture_cloth.outputFolder = './textureCloth/'
    l23_texture_cloth.run()

if __name__ == '__main__':
    main()
