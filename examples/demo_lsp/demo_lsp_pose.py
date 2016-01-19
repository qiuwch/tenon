# Demo script to show how to use tenon
tenonpath = '/q/workspace/tenon'
import sys; sys.path.append(tenonpath) # Install tenon
import tenon
import random
sys.path.append('.')
import lsppose

def setup_scene():
    # Create pose constraints
    lsppose.createConstraint()

    # Setup lighting for the scene
    radius = 12
    nLight = 16
    z = 10
    lamps = [tenon.obj.Lamp.create('light%d' % v) for v in range(10)]
    for i in range(len(lamps)):
        lamp = lamps[i]

        # Compute the location of light source, put the light evenly
        lampObj = tenon.obj.get(lamp.name)
        lampObj.location = tenon.util.sphereLocation(radius, 360 / nLight * i, 0)
        lampObj.location[2] += z  # Set the z of the light source

    scene = tenon.util.dictwrapper(lamps = lamps)
    return scene

def update_scene(scene, poseid):
    # Update human pose
    lsppose.animate('./2015101415_v2/%04d.csv' % poseid)

    # Randomly update lighting
    for l in scene.lamps:
        l.energy = random.gauss(1, 1.5)


def main():
    sys.path.append('/q/workspace/tenon/examples/')

    camera = tenon.obj.get('Camera')
    scene = setup_scene()

    for i in range(10):
        update_scene(scene, i)
        tenon.render.write('fig/demo_lsp_pose_%d.png' % i)

tenon.run(__file__, 'demo_human.blend')
if tenon.inblender():
    main()

# Define a scene first, then apply scene spefic operation.
