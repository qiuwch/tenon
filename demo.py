# Demo script to show how to use tenon
# Use tenon
# 1. headless mode for rendering
# 2. interactive in blender shell
import sys, os
sys.path.append(os.path.expanduser('~/Dropbox/workspace/tenon/code'))
import tenon

def main():
    import tenon.logging as L
    import bpy

    camera = tenon.obj.get('Camera')
    # none_exist_obj = tenon.obj.get('none_exist')
    print(camera.location)
    for i in range(10):
        camera.location.x += 1
        figname = '../cache/fig/demo%d.png' % i
        tenon.render.write(figname)
        L.info('Write to %s successful' % figname)
    # objs = dict(camera='Camera')

if not tenon.inblender():
    tenon.run(__file__, 'demo.blend')
else:
    main()

# Define a scene first, then apply scene spefic operation.
