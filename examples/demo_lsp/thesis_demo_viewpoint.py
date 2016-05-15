# Demo script to show how to use tenon

# Define global variables
import sys, os
pwd = os.getcwd()
rootdir = os.path.join(pwd, '../../..') # This folder is /examples/demo_lsp/
tenonpath = os.path.join(rootdir, 'code')
outputdir = os.path.join(rootdir, 'cache/lsp_synthesized')
print(tenonpath)
sys.path.append(os.path.expanduser(tenonpath))

import tenon
sys.path.append(pwd)
import lsppose

import argparse

def main():
    util = lsppose.Util()
    models = lsppose.Models()
    util.rootdir = rootdir

    import tenon.logging as L
    # outputdir = '//../cache/lsp_synthesized'
    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')
    tenon.render.write('init.png')

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
    schedule_idx = [2]
    for i in schedule_idx:
        util.update_scene(scene, i)

        # imgfilename = os.path.join(outputdir, 'imgs/%04d.png' % i)
        # tenon.render.write(imgfilename)
        # L.info('Synthetic image: %s' % L.prettify_filename(imgfilename))

        # depth_filename = os.path.join(outputdir, 'depth/%04d.png' % i)
        # tenon.render.DepthMode.enable()
        # tenon.render.write(depth_filename)
        # L.info('Depth: %s' % L.prettify_filename(depth_filename))
        # tenon.render.DepthMode.disable()

        # paint_filename = os.path.join(outputdir, 'parts/%04d.png' % i)
        # for obj in objs:
        #     tenon.render.PaintMode.enable(obj)
        # tenon.render.write(paint_filename)
        # L.info('Semantic parts: %s' % L.prettify_filename(paint_filename))
        # for obj in objs:
        #     tenon.render.PaintMode.disable(obj)

        # # Also save the joint annotation and part annotation
        # joint_filename = os.path.join(outputdir, 'joints/%04d.csv' % i)
        # joints = lsppose.JointInfo.export()
        # lsppose.JointInfo.serializeJointInfo(joint_filename, joints)

        import tenon.util as U
        radius = camera.location.length # Keep the radius fixed
        el = 0
        # for angle in [0, 90, 180, 270]:
        # for angle in range(0, 360, 10):
        for angle in [240]:
            for el in range(0, 90, 10):
                loc = U.sphere_location(radius, angle, el)
                camera.location = loc
                imgfilename = os.path.join(outputdir, 'imgs/%04d_%d_%d.png' % (i, angle, el))
                tenon.render.write(imgfilename)
                L.info('Synthetic image: %s' % L.prettify_filename(imgfilename))


if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--blendfile', default = os.path.join(rootdir, 'data/fully_annotated.blend'))

        args = parser.parse_args()
        tenon.run(__file__, args.blendfile)
    else:
        main()
