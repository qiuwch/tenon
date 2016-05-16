import skimage.io
import numpy as np
import random
import os

N = 10000
w = 100
h = 100

for i in range(N):
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    
    im = np.ones((h, w, 3))
    im[:,:,0] = r
    im[:,:,1] = g
    im[:,:,2] = b
    skimage.io.imsave(os.path.join('randomColor', '%d.png' % i), im)