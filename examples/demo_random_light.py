# Demo script to show how to generate random lighting
import sys, os
# sys.path.append(os.path.expanduser('~/Dropbox/workspace/tenon/code'))
sys.path.append(os.path.abspath('..'))
import tenon

rootdir = './../../'
def main():
    import random
    import tenon.logging as L
    # L.fileLevel(L.DEBUG) # default is ERROR
    cachedir = os.path.abspath(os.path.join(rootdir, 'cache/examples/random_light'))

    # Set up the light configuration
    radius = 12
    nLight = 16
    z = 10
    lamps = [tenon.obj.Lamp.create('light%d' % v) for v in range(10)]

    for j in range(10):
        for i in range(len(lamps)):
            lamp = lamps[i]

            # Compute the location of light source, put the light evenly
            lampObj = tenon.obj.get(lamp.name)
            lampObj.location = tenon.util.sphereLocation(radius, 360 / nLight * i, 0)
            lampObj.location[2] += z  # Set the z of the light source
            lamp.energy = random.gauss(1, 1.5)
        filename = os.path.join(cachedir, 'random_lighting_%d.png' % j)
        L.info('Rendered file: %s', filename)
        tenon.render.write(filename)

if not tenon.inblender():
    scenefile = os.path.join(rootdir, 'code/demo.blend')
    tenon.run(__file__, scenefile)
else:
    main()
