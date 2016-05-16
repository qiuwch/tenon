# Demo script to show how to use tenon

# Define global variables
import sys, os

# Define the paths where python can find tenon and lsppose
paths = [os.path.abspath('../..'), os.path.abspath('.')]
[sys.path.append(p) for p in paths]
import tenon
import lsppose

import argparse

def main():
    outputdir = './images'
    util = lsppose.Util()
    models = lsppose.Models()
    util.rootdir = rootdir

    import tenon.logging as L
    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')
    tenon.render.write('init.png')
    return

    camera = tenon.obj.get('Camera') # Unused in this demo
    scene = util.setup_scene()

    objs = [
        # models.humanModel(),
        models.bodyMesh(),
        models.upperCloth(),
        models.lowerCloth(),
        models.hair(),
        models.eye()
        ]

    schedule_idx = range(1, 20001)
    schedule_idx = [73]
    for i in schedule_idx:
        util.update_scene(scene, i)

        imgfilename = os.path.join(outputdir, 'imgs/%04d.png' % i)
        tenon.render.write(imgfilename)
        L.info('Synthetic image: %s' % L.prettify_filename(imgfilename))

        depth_filename = os.path.join(outputdir, 'depth/%04d.png' % i)
        tenon.render.DepthMode.enable()
        tenon.render.write(depth_filename)
        L.info('Depth: %s' % L.prettify_filename(depth_filename))
        tenon.render.DepthMode.disable()

        paint_filename = os.path.join(outputdir, 'parts/%04d.png' % i)
        for obj in objs:
            tenon.render.PaintMode.enable(obj)
        tenon.render.write(paint_filename)
        L.info('Semantic parts: %s' % L.prettify_filename(paint_filename))
        for obj in objs:
            tenon.render.PaintMode.disable(obj)

        # Also save the joint annotation and part annotation
        joint_filename = os.path.join(outputdir, 'joints/%04d.csv' % i)
        joints = lsppose.JointInfo.export()
        lsppose.JointInfo.serializeJointInfo(joint_filename, joints)


if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--blendfile', default = os.path.join('../data/mocap_demo_scene.blend'))

        args = parser.parse_args()
        tenon.run(__file__, args.blendfile)
    else:
        main()
