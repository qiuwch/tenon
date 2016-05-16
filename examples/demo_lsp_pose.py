# Demo script to show how to generate synthetic human images
import sys, os, argparse

# Define the paths where python can find tenon and lsppose
paths = [os.path.abspath('..'), os.path.abspath('demo_lsp')]
[sys.path.append(p) for p in paths]
import tenon
import tenon.logging as L
import lsppose

def main():
    out_folders = {
        'image': './lsp/images',
        'depth': './lsp/depth',
        'semantic': './lsp/semantic',
        '2dpose': './lsp/2dpose'
    }
    for path in out_folders.values():
        if not os.path.exists(path):
            os.makedirs(path)

    util = lsppose.Util()
    models = lsppose.Models()

    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')
    L.info('Write a test image to init.png')
    tenon.render.write('lsp/init.png')

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

    schedule_idx = range(1, 2001)
    schedule_idx = [73]
    for pose_id in schedule_idx:
        posefolder = '../data/2015101415_v2'
        util.update_scene(posefolder, scene, pose_id)

        imgfilename = os.path.join(out_folders['image'], '%04d.png' % pose_id)
        tenon.render.write(imgfilename)
        L.info('Synthetic image: %s' % L.prettify_filename(imgfilename))

        depth_filename = os.path.join(out_folders['depth'], '%04d.png' % pose_id)
        tenon.render.DepthMode.enable()
        tenon.render.write(depth_filename)
        L.info('Depth: %s' % L.prettify_filename(depth_filename))
        tenon.render.DepthMode.disable()

        paint_filename = os.path.join(out_folders['semantic'], '%04d.png' % pose_id)
        for obj in objs:
            tenon.render.PaintMode.enable(obj)
        tenon.render.write(paint_filename)
        L.info('Semantic parts: %s' % L.prettify_filename(paint_filename))
        for obj in objs:
            tenon.render.PaintMode.disable(obj)

        # Also save the joint annotation and part annotation
        joint_filename = os.path.join(out_folders['2dpose'], '%04d.csv' % pose_id)
        joints = lsppose.JointInfo.export()
        lsppose.JointInfo.serializeJointInfo(joint_filename, joints)
        L.info('2D joint location: %s' % L.prettify_filename(joint_filename))

if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--blendfile', default = os.path.join('../data/fully_annotated.blend'))

        args = parser.parse_args()
        tenon.run(__file__, args.blendfile)
    else:
        main()
