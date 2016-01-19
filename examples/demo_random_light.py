# Demo script to show how to generate random lighting
tenonpath = '/q/workspace/tenon'
import sys; sys.path.append(tenonpath) # Install tenon
import tenon

def main():
    import random

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
        tenon.render.write('fig/random_lighting_%d.png' % j)


tenon.run(__file__, '../demo.blend')
if tenon.inblender():
    main()
