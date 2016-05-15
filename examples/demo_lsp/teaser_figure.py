import os
import matplotlib.pyplot as plt
import numpy as np
import skimage.transform as T
import ipdb
import logging as L
from postprocess import Cropper
cropper = Cropper()

L.basicConfig(level=L.INFO)

lsp_folder = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/thesis/synthesis_pipeline/cache/lsp_synthesized/')

def draw_skeleton(cropped_coords):
    x = [p[0] for p in cropped_coords]
    y = [p[1] for p in cropped_coords]
    plt.plot(x, y, '*', scalex=False, scaley=False)

    # The input order is defined in http://www.comp.leeds.ac.uk/mat4saj/lsp.html
    A = [1, 2, 4, 5, 7, 8, 10, 11, 13, 13, 13, 3, 4]  # The point a of a bone
    B = [2, 3, 5, 6, 8, 9, 11, 12, 14, 9,  10, 9, 10]
    # for i in range(len(A)):
    for i in range(len(A)-1, -1, -1):
        point_a = cropped_coords[A[i]-1]
        point_b = cropped_coords[B[i]-1]
        plt.plot([point_a[0], point_b[0]], [point_a[1], point_b[1]], linewidth=1, scalex=False, scaley=False)

def crop_file(i):
    joint_file = os.path.join(lsp_folder, 'joints', '%04d.csv' % i)
    fullimg_filename = os.path.join(lsp_folder, 'imgs', '%04d.png' % i)
    cropped_filename = os.path.join(lsp_folder, 'cropped', '%04d.png' % i)
    depth_filename = os.path.join(lsp_folder, 'depth', '%04d.png' % i)
    part_filename = os.path.join(lsp_folder, 'parts', '%04d.png' % i)
    real_filename = os.path.expanduser('~/Dropbox/dataset/lsp/lsp_dataset/images/im%04d.jpg' % i)

    X = []; Y = []; labels = []
    with open(joint_file) as f:
        for l in f:
            [label, x, y] = l.strip().split(',')
            X.append(int(x))
            Y.append(int(y))
            labels.append(label)
            L.debug('label %s, x: %d, y: %d', label, x, y)

    depth = plt.imread(depth_filename);
    depth = depth[:,:,0]

    fullimg = plt.imread(fullimg_filename)
    partimg = plt.imread(part_filename)
    realimg = plt.imread(real_filename)
    orig_coords = np.array([X, Y]).T

    [cropped_img, cropped_coords] = cropper.crop_img(fullimg, depth, orig_coords, labels)
    [cropped_depth, tmp] = cropper.crop_img(depth, depth, orig_coords, labels)
    [cropped_parts, tmp] = cropper.crop_img(partimg, depth, orig_coords, labels)

    plt.subplot(1,5,1)
    plt.imshow(cropped_img)
    plt.axis('off')
    plt.subplot(1,5,2)
    plt.imshow(cropped_depth, cmap='Greys_r')
    plt.axis('off')
    plt.subplot(1,5,3)
    plt.imshow(cropped_img * 0)
    draw_skeleton(cropped_coords)
    plt.axis('off')
    plt.subplot(1,5,4)
    plt.imshow(cropped_parts)
    plt.axis('off')
    plt.subplot(1,5,5)
    plt.imshow(realimg)
    plt.axis('off')
    # plt.show()
    plt.savefig('teaser_figure.png')

# id = 73
id = 2
crop_file(id)
