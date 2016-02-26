# Demo script to show how to use tenon
# Define global variables
import tenon.logging as L
L.setLevel(L.INFO)

import sys, os
rootdir = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon')
tenonpath = os.path.join(rootdir, 'code/tenon')
pwd = os.path.join(rootdir, 'code/tenon/examples/demo_lsp')
output_dir = os.path.join(rootdir, 'cache/lsp_synthesized/circular_demo')

for v in [tenonpath, pwd]:
    sys.path.append(os.path.expanduser(v))
import tenon
import lsppose

# L.setLevel(L.DEBUG)

def blender():
    lsppose_ = lsppose.Util()
    lsppose_.rootdir = rootdir

    import tenon.util as U

    L.info('Switch logging level to INFO')

    camera = tenon.obj.get('Camera') # Unused in this demo
    scene = lsppose_.setup_scene()

    lsppose_.update_scene(scene, 1)


    radius = camera.location.length # Keep the radius fixed
    el = 0
    i = 1
    for az in range(0, 360, 90):
        loc = U.sphere_location(radius, az, el)
        camera.location = loc

        filename_no_ext = '%04d_az%d' % (i, az)
        lsppose_.render_scene(os.path.join(output_dir, 'full'), filename_no_ext)
        # Generate cropped version also


def postprocess():
    '''
    Pose process which needs to be run outside of blender
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    import tenon.logging as L
    i = 1
    az = 0
    filename_no_ext = '%04d_az%d' % (i, az)
    joint_file = os.path.join(output_dir, 'full', 'joints', '%s.csv' % filename_no_ext)
    fullimg_filename = os.path.join(output_dir, 'full', 'imgs', '%s.png' % filename_no_ext)
    # cropped_filename = os.path.join(output_dir, 'cropped', '%s.png' % filename_no_ext)
    depth_filename = os.path.join(output_dir, 'full', 'depth', '%s.png' % filename_no_ext)

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
    cropper = lsppose.Cropper()
    [cropped_img, cropped_coords] = cropper.crop_img(fullimg, depth, orig_coords)
    combine_img = cropper.add_bg(cropped_img, 0)

    L.info('Crop file %s', fullimg_filename)
    plt.subplot(1,2,1)
    plt.imshow(cropped_img)
    plt.subplot(1,2,2)
    plt.imshow(combine_img)
    plt.show()

if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        scenefile = os.path.join(rootdir, 'data/mocap_demo_scene.blend')
        tenon.run(__file__, scenefile)
        postprocess()
    else:
        blender()
