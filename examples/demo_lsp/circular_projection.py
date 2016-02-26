# Demo script to show how to use tenon

# Define global variables
import sys, os
rootdir = '~/Dropbox/workspace/graphics_for_vision/tenon'
tenonpath = os.path.join(rootdir, 'code')
pwd = os.path.join(rootdir, 'code/examples/demo_lsp')
for v in [tenonpath, pwd]:
    sys.path.append(os.path.expanduser(v))
import tenon
import lsppose


def main():
    lsppose_ = lsppose.Util()
    lsppose_.rootdir = rootdir

    import tenon.logging as L
    import tenon.util as U

    outputdir = '//../cache/lsp_synthesized/circular_demo'
    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')

    camera = tenon.obj.get('Camera') # Unused in this demo
    scene = lsppose_.setup_scene()

    lsppose_.update_scene(scene, 1)


    radius = camera.location.length # Keep the radius fixed
    el = 0
    i = 1
    for az in range(0, 360, 30):
        loc = U.sphere_location(radius, az, el)
        camera.location = loc

        imgfilename = os.path.join(outputdir, 'imgs/%04d_az%d.png' % (i, az))
        L.info('Render file to %s', U.pretify_filename(imgfilename))
        tenon.render.write(imgfilename)

        depth_filename = os.path.join(outputdir, 'depth/%04d_az%d.png' % (i, az))
        tenon.render.DepthMode.enable()
        tenon.render.write(depth_filename)
        tenon.render.DepthMode.disable()

        paint_filename = os.path.join(outputdir, 'parts/%04d_az%d.png' % (i, az))
        tenon.render.PaintMode.enable(lsppose.models.humanModel())
        tenon.render.write(paint_filename)

        # Also save the joint annotation and part annotation
        joint_filename = os.path.join(outputdir, 'joints/%04d_az%d.csv' % (i, az))
        joints = lsppose.JointInfo.export()
        lsppose.JointInfo.serializeJointInfo(joint_filename, joints)


if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        scenefile = os.path.join(rootdir, 'data/mocap_demo_scene.blend')
        tenon.run(__file__, scenefile)
    else:
        main()
