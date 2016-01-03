import sys
sys.path.append('../../tenon/')
import util

import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import skimage.io
import numpy as np
import argparse

def composite(nobgfolder):
    nobgfolderCrop = os.path.join(nobgfolder, 'crop')
    compositefolder = os.path.join(nobgfolderCrop, 'composite')
    # nobgfolder = '/q/cache/tenon/rendered/no_bg_1128/crop/'
    # compositefolder = '/q/cache/tenon/rendered/no_bg_1128/crop/composite/'

    if not os.path.isdir(compositefolder):
        os.mkdir(compositefolder)
        
    nobgfiles = glob.glob(os.path.join(nobgfolderCrop, 'imgs/*.png'))
    bgfolder = '/q/data/INRIA/'
    bgfiles = glob.glob(bgfolder + '*.jpg')

    pg = util.ProgressBar(len(nobgfiles))
    for i in range(len(nobgfiles)):
        pg.update(i)
        nobgfile = nobgfiles[i]
        im = skimage.io.imread(nobgfile)
        alpha = im[:,:,3]
        im = im[:,:,0:3]    
        [h, w, c] = im.shape
        
        bgid = random.randint(0, len(bgfiles)-1)
        bgfile = bgfiles[bgid]
        # bg = plt.imread(bgfile)
        bg = skimage.io.imread(bgfile)
        assert(im.dtype == bg.dtype)
        bgCrop = bg[0:h, 0:w, :]

        fgmask = np.tile(alpha[:,:,np.newaxis] / 255.0, (1, 1, 3));
        bgmask = 1 - fgmask;
        combine = bgCrop * bgmask + im * fgmask
        combine = combine.astype('uint8')
        
        combinefile = os.path.join(compositefolder, os.path.basename(nobgfile))
        skimage.io.imsave(combinefile, combine)

def main():
    parser = argparse.ArgumentParser(description = 'Add random background to no bg images')
    parser.add_argument('nobgfolder', help='Image without bg')

    args = parser.parse_args()
    composite(args.nobgfolder)

if __name__ == '__main__':
    main()
