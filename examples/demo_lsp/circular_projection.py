'''
Synthesize images around the center object
'''
import sys, os
rootdir = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon')
tenonpath = os.path.join(rootdir, 'code/tenon')
pwd = os.path.join(rootdir, 'code/tenon/examples/demo_lsp')
for v in [tenonpath, pwd]:
    sys.path.append(os.path.expanduser(v))
import tenon
import lsppose

# output_dir = os.path.join(rootdir, 'cache/lsp_synthesized/circular_demo')
output_dir = os.path.expanduser('~/nosync/circular_demo/')

import tenon.logging as L
L.setLevel(L.INFO)
# L.setLevel(L.DEBUG)
L.info('Output folder is %s', L.prettify_filename(output_dir))


def blender():
    lsppose_ = lsppose.Util()
    lsppose_.rootdir = rootdir

    import tenon.util as U

    L.info('Switch logging level to INFO')

    camera = tenon.obj.get('Camera') # Unused in this demo
    scene = lsppose_.setup_scene()

    radius = camera.location.length # Keep the radius fixed
    el = 0
    for i in range(143, 2001):
        lsppose_.update_scene(scene, i)
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
    i = 1
    for i in range(1, 2001):
        for az in range(0, 360, 90):
            postprocess_img(i, az)

def postprocess_img(i, az):
    import matplotlib.pyplot as plt
    import numpy as np
    import tenon.logging as L

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
            L.debug('label %s, x: %s, y: %s', label, x, y)

    # Get scale and translation parameters

    depth = plt.imread(depth_filename);
    depth = depth[:,:,0]
    fullimg = plt.imread(fullimg_filename)
    orig_coords = np.array([X, Y]).T
    cropper = lsppose.Cropper()
    [cropped_img, cropped_coords] = cropper.crop_img(fullimg, depth, orig_coords, labels)
    combine_img = cropper.add_bg(cropped_img)

    L.info('Crop file %s', fullimg_filename)
    if L.isDebug() and False:
        plt.subplot(1,2,1)
        plt.imshow(cropped_img)
        plt.subplot(1,2,2)
        plt.imshow(combine_img)
        plt.show()

    cropped_filename = os.path.join(output_dir, 'crop', 'nobg', '%s.png' % filename_no_ext)
    cropped_filename_bg = os.path.join(output_dir, 'crop', 'imgs', '%s.png' % filename_no_ext)
    cropped_joints = os.path.join(output_dir, 'crop', 'joints', '%s.csv' % filename_no_ext)
    plt.imsave(cropped_filename, cropped_img)
    plt.imsave(cropped_filename_bg, combine_img)

    L.info('Cropped image %s\nCropped joint info %s', L.prettify_filename(cropped_filename_bg), \
            L.prettify_filename(cropped_joints))
    L.debug('Shape of cropped_coords %s', cropped_coords.shape)
    with open(cropped_joints, 'w') as f:
        for i in range(cropped_coords.shape[0]):
            f.write('%.2f,%.2f\n' % (cropped_coords[i,0], cropped_coords[i,1]))

if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        scenefile = os.path.join(rootdir, 'data/mocap_demo_scene.blend')
        # tenon.run(__file__, scenefile)
        postprocess()
    else:
        blender()
