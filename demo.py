'''
This script will render a few images with different camera positions for a very simple scene.
'''
import sys, os

# To use this library, need to append the absolute path of this folder
sys.path.append(os.getcwd())
import tenon

def main():
    import tenon.logging as L
    import bpy

    camera = tenon.obj.get('Camera')
    # check demo.blend to get the camera name
    for i in range(10):
        camera.location.x += 1
        # L.info(camera.location)
        figname = './data/demo/%04d.png' % i
        tenon.render.write(figname)
        # TODO: Generate html doc from source code
        L.info('Write to %s successful' % figname)

if not tenon.inblender():
    tenon.run(__file__, './data/simple_demo.blend')
else:
    main()
