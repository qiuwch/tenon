import logging as L
import os, glob
class Cropper: # This may need to run outside of blender
    def __init__(self):
        self.joint_mapping = None
        self.bgfiles = None

    def transform_matrix(self, depth):
        import numpy as np
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

    def get_joint_mapping(self, labels):
        import numpy as np
        if self.joint_mapping == None:
            LSP_order = [
                'shin.fk.R.tail',      'thigh.fk.R.tail', 'thigh.fk.R.head',
                'thigh.fk.L.head',     'thigh.fk.L.tail', 'shin.fk.L.tail',
                'forearm.fk.R.tail',   'upper_arm.fk.R.tail', 'upper_arm.fk.R.head',
                'upper_arm.fk.L.head', 'upper_arm.fk.L.tail', 'forearm.fk.L.tail',
                'neck.head',           'head.tail'
            ]

            mapping = []
            for v in LSP_order:
                index = labels.index(v)
                mapping.append(index)
            L.debug('The label mapping is %s' % mapping)
            self.joint_mapping = np.array(mapping)

        # ipdb.set_trace()
        return self.joint_mapping

    def crop_img(self, fullimg, depth, orig_coords, orig_labels):
        import numpy as np
        import skimage.transform as T
        [crop_height, crop_width, mat] = self.transform_matrix(depth)
        transform_mat = np.linalg.inv(mat)

        L.debug('Final transform matrix\n%s', transform_mat)
        cropped_img = T.warp(fullimg, transform_mat, output_shape=np.round((crop_height, crop_width)), order=3)
        # Bicubic, default is 1, bilinear

        cropped_coords = T.matrix_transform(orig_coords, mat)

        L.debug('Original coords %s', orig_coords)
        L.debug('Transformed coords %s', cropped_coords)
        # T.matrix_transform() # Use this to tranform coordinate

        index_mapping = self.get_joint_mapping(orig_labels)
        # index_mapping = np.array([6, 1, 3, 2, 0, 5, 8, 10, 12, 11, 9, 7, 13, 4])
        # The order for LSP dataset
        # PC format
        # The order is defined in here: http://www.comp.leeds.ac.uk/mat4saj/lsp.html
        L.debug('Transformed labels %s', [orig_labels[v] for v in index_mapping])

        resorted_cropped_coords = cropped_coords[index_mapping, :]
        L.debug('Transformed LSP coords\n%s', resorted_cropped_coords)
        # L.debug('Transformed joint labels %s', [labels[i] for i in index_mapping])
        return [cropped_img, resorted_cropped_coords]


    def get_bgfiles(self):
        bgfolder = os.path.expanduser('~/Dropbox/dataset/INRIA/')
        L.info('Get background images from %s', bgfolder)
        if self.bgfiles == None:
            self.bgfiles = glob.glob(os.path.join(bgfolder, '*.jpg'))

        return self.bgfiles


    def add_bg(self, nobgimg, bgid=None):
        '''
        Add background to the rendered image
        The sky option in 'Render Layers' needs to be disabled
        '''
        import skimage.io
        from skimage import img_as_float
        import random
        import numpy as np

        if isinstance(nobgimg, str):
            nobgimg = skimage.io.imread(nobgimg)


        im = nobgimg
        alpha = im[:,:,3]
        im = im[:,:,0:3]
        [h, w, c] = im.shape

        bgfiles = self.get_bgfiles()
        if bgid is None:
            bgid = random.randint(0, len(bgfiles)-1)
        bgfile = bgfiles[bgid]
        L.debug('BG id is %d', bgid)

        # bg = plt.imread(bgfile)
        bg = skimage.io.imread(bgfile)
        bg = img_as_float(bg)
        im = img_as_float(im)
        assert im.dtype == bg.dtype, 'im type %s and bg type %s' % (im.dtype, bg.dtype)
        bgCrop = bg[0:h, 0:w, :]

        L.debug('The range of alpha is (%f, %f)', alpha.min(), alpha.max())
        fgmask = np.tile(alpha[:,:,np.newaxis], (1, 1, 3));
        bgmask = 1 - fgmask;
        combine = bgCrop * bgmask + im * fgmask

        if L.isDebug():
            L.debug('Show the images for composite')
            import matplotlib.pyplot as plt
            plt.subplot(2,2,1)
            plt.imshow(im)
            plt.subplot(2,2,2)
            plt.imshow(bgCrop)
            plt.subplot(2,2,3)
            plt.imshow(combine)
            plt.show()


        return combine