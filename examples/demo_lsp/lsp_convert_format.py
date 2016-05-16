# Convert from full size image to cropped humans
import os
import matplotlib.pyplot as plt
import numpy as np
import skimage.transform as T
import ipdb
import logging as L

L.basicConfig(level=L.INFO)

if __name__ == '__main__':
    lsp_folder = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon/cache/lsp_synthesized/')

    def crop_file(i):
        joint_file = os.path.join(lsp_folder, 'joints', '%04d.csv' % i)
        fullimg_filename = os.path.join(lsp_folder, 'imgs', '%04d.png' % i)
        cropped_filename = os.path.join(lsp_folder, 'cropped', '%04d.png' % i)
        depth_filename = os.path.join(lsp_folder, 'depth', '%04d.png' % i)

        X = []; Y = []; labels = []
        with open(joint_file) as f:
            for l in f:
                [label, x, y] = l.strip().split(',')
                X.append(int(x))
                Y.append(int(y))
                labels.append(label)
                L.debug('label %s, x: %d, y: %d', label, x, y)

        # Get scale and translation parameters

        depth = plt.imread(depth_filename);
        depth = depth[:,:,0]
        # fg_mask = depth > 0;
        # plt.imshow(fg_mask)

        # Construct a tranform matrix
        # Get the human bbox

        # Crop image
        # Get a rectangle region from the image
        fullimg = plt.imread(fullimg_filename)
        orig_coords = np.array([X, Y]).T
        [cropped_img, cropped_coords] = crop_img(fullimg, depth, orig_coords)

        plt.subplot(1,2,1)
        plt.imshow(fullimg)
        plt.axis('off')
        plt.subplot(1,2,2)
        plt.imshow(cropped_img)
        plt.axis('off')
        plt.show()
        plt.imsave(cropped_filename, cropped_img)

    for i in range(1, 10):
        crop_file(i)
