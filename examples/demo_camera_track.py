'''
Demo script to show how to change the camera position while keeps tracking a target object
'''
import sys, os
sys.path.append(os.path.abspath('..'))
import tenon

rootdir = './../../'
def main():
    import tenon.logging as L
    import tenon.util as U

    L.setLevel(L.DEBUG)
    cachedir = os.path.abspath(os.path.join(rootdir, 'cache/examples/camera_track'))

    # Set up the camera tracking constraint
    # The object will be out of the view without setting a proper tracking constraint
    camera = tenon.obj.get('Camera')
    target = tenon.obj.get('Suzanne')
    # tenon.constraint.TrackConstraint()

    # Track_to constraint
    U.camera_track(camera, target) # Setup camera tracking constraint

    # Set up the light configuration
    for count in range(10):
        camera.location.x -= 0.5

        filename = os.path.join(cachedir, 'camera_track_%d.png' % count)
        tenon.render.write(filename)


    radius = camera.location.length # Keep the radius fixed
    el = 0
    for az in range(0, 360, 30):
        loc = U.sphere_location(radius, az, el)
        camera.location = loc

        filename = os.path.join(cachedir, 'circular_az%d.png' % az)
        tenon.render.write(filename)

if not tenon.inblender():
    scenefile = os.path.join(rootdir, 'code/demo.blend')
    tenon.run(__file__, scenefile)
else:
    main()
