import numpy as np
import matplotlib.pyplot as plt
import os

lsp_folder = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon/cache/lsp_synthesized/')

i = 1
joint_file = os.path.join(lsp_folder, 'joints', '%04d.csv' % i)
fullimg_filename = os.path.join(lsp_folder, 'imgs', '%04d.png' % i)
im = plt.imread(fullimg_filename)

X = []; Y = []
with open(joint_file) as f:
    for l in f:
        [name, x, y] = l.strip().split(',')
        X.append(int(x))
        Y.append(int(y))
        print name, x, y

plt.imshow(im)
plt.plot(X, Y, '*')
# Need to connect the joint annotation to stick
plt.show()

