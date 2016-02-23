# Demo script to show how to use tenon

# Define global variables
rootdir = '~/Dropbox/workspace/graphics_for_vision/tenon'
tenonpath = '~/Dropbox/workspace/graphics_for_vision/tenon/code'
pwd = '/home/qiuwch/Dropbox/workspace/graphics_for_vision/tenon/code/examples/demo_lsp'
import sys, os
sys.path.append(os.path.expanduser(tenonpath))
import tenon
sys.path.append(pwd)
import lsppose

import random

def create_lamps():
    # Setup lighting for the scene
    radius = 12
    nLight = 16
    z = 10
    lamps = [tenon.obj.Lamp.create('light%d' % v) for v in range(nLight)]
    for i in range(len(lamps)):
        lamp = lamps[i]

        # Compute the location of light source, put the light evenly
        lampObj = tenon.obj.get(lamp.name)
        lampObj.location = tenon.util.sphereLocation(radius, 360.0 / nLight * i, 0)
        lampObj.location[2] += z  # Set the z of the light source

    return lamps

def setup_scene():
    # Create pose constraints
    # The contraint point will be initially put on the 3D cursor
    lsppose.createConstraint()

    lamps = create_lamps()

    scene = tenon.util.dictwrapper(lamps = lamps)
    return scene

def update_scene(scene, poseid):
    # Update human pose
    lsppose.animate(os.path.join(rootdir, 'data', '2015101415_v2/%04d.csv' % poseid))

    # Randomly update lighting
    for l in scene.lamps:
        l.energy = random.gauss(1, 1.5)

def main():
    import tenon.logging as L
    outputdir = '//../cache/lsp_synthesized'
    L.setLevel(tenon.logging.INFO)
    L.info('Switch logging level to INFO')
    tenon.render.write('init.png')

    camera = tenon.obj.get('Camera')
    scene = setup_scene()

    for i in range(1, 2001):
        update_scene(scene, i)

        imgfilename = os.path.join(outputdir, 'imgs/%04d.png' % i)
        tenon.render.write(imgfilename)

        depth_filename = os.path.join(outputdir, 'depth/%04d.png' % i)
        tenon.render.DepthMode.enable()
        tenon.render.write(depth_filename)
        tenon.render.DepthMode.disable()

        paint_filename = os.path.join(outputdir, 'parts/%04d.png' % i)
        tenon.render.PaintMode.enable(tenon.obj.get('Suzanne'))
        tenon.render.write(paint_filename)

        # Also save the joint annotation and part annotation
        joint_filename = os.path.join(outputdir, 'joints/%04d.csv' % i)
        joints = lsppose.JointInfo.export()
        lsppose.JointInfo.serializeJointInfo(joint_filename, joints)


if __name__ == '__main__':
    # Avoid execution during module import
    if not tenon.inblender():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('scenefile', default = os.path.join(rootdir, 'data/mocap_demo_scene.blend'), help = 'The scene file for rendering')

        args = parser.parse_args()

        tenon.run(__file__, args.scenefile)
    else:
        main()
