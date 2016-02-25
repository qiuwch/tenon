'''
Demo script to show how to change the camera position while keeps tracking a target object
'''
import sys, os
sys.path.append(os.path.abspath('..'))
import tenon

rootdir = './../../'
def main():
    import random
    import tenon.logging as L
    L.setLevel(L.DEBUG)
    cachedir = os.path.abspath(os.path.join(rootdir, 'cache/examples/camera_track'))

    # Set up the camera tracking constraint
    # The object will be out of the view without setting a proper tracking constraint
    camera = tenon.obj.get('Camera')
    target = tenon.obj.get('Suzanne')
    # tenon.constraint.TrackConstraint()

    # Track_to constraint
    c = camera.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'

    # Set up the light configuration
    for count in range(10):
        camera.location.x -= 0.5

        filename = os.path.join(cachedir, 'camera_track_%d.png' % count)
        tenon.render.write(filename)

if not tenon.inblender():
    scenefile = os.path.join(rootdir, 'code/demo.blend')
    tenon.run(__file__, scenefile)
else:
    main()
