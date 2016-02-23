import os
import matplotlib.pyplot as plt
import numpy as np
import skimage.transform as T
import ipdb
import logging as L

L.basicConfig(level=L.INFO)

def transform_matrix(depth):
    [y, x] = np.where(depth > 0)
    h = max(y) - min(y) + 1
    w = max(x) - min(x) + 1

    margin_ratio = 0.1
    crop_margin = max(h, w) * margin_ratio
    crop_width = w + 2 * crop_margin
    crop_height = h + 2 * crop_margin

    # target_size = 150.0 # TODO: This size will create very jagg boundary
    target_size = 300.0
    scale = target_size / max(crop_width, crop_height)

    crop_width *= scale
    crop_height *= scale

	# Translation in x, map (min(X) - margin) to 1, what will happen in it is smaller than 1
    tx = - scale * (min(x) - crop_margin) + 1;
    ty = - scale * (min(y) - crop_margin) + 1;
    L.debug('min(x) %f  max(x) %f', min(x), min(y))
    # ipdb.set_trace()

    matrix = np.array([[scale, 0, tx], [0, scale, ty], [0, 0, 1]])
    L.debug('Original transform matrix\n%s', matrix)
    return [crop_height, crop_width, matrix]

def crop_img(fullimg, depth, orig_coords):
    [crop_height, crop_width, mat] = transform_matrix(depth)
    transform_mat = np.linalg.inv(mat)

    L.debug('Final transform matrix\n%s', transform_mat)
    cropped_img = T.warp(fullimg, transform_mat, output_shape=np.round((crop_height, crop_width)), order=3)
    # Bicubic, default is 1, bilinear

    cropped_coords = T.matrix_transform(orig_coords, mat)

    L.debug('Original coords %s', orig_coords)
    L.debug('Transformed coords %s', cropped_coords)
    # T.matrix_transform() # Use this to tranform coordinate

    index_mapping = np.array([6, 1, 3, 2, 0, 5, 8, 10, 12, 11, 9, 7, 13, 4])
    lsp_cropped_coords = cropped_coords[index_mapping, :]
    L.debug('Transformed LSP coords %s', lsp_cropped_coords)
    # L.debug('Transformed joint labels %s', [labels[i] for i in index_mapping])
    return [cropped_img, cropped_coords]

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

