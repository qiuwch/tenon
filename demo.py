# Demo script to show how to use tenon
# Use tenon
# 1. headless mode for rendering
# 2. interactive in blender shell
tenonpath = '/q/workspace/tenon'
import sys; sys.path.append(tenonpath) # Install tenon
import tenon

def main():
    import tenon.logging as L
    if tenon.inblender():
        import bpy

    camera = tenon.obj.get('Camera')
    # none_exist_obj = tenon.obj.get('none_exist')
    print(camera.location)
    for i in range(10):
        camera.location.x += 1
        figname = 'fig/demo%d.png' % i
        tenon.render.write(figname)
        L.info('Write to %s successful' % figname)
    # objs = dict(camera='Camera')

tenon.run(__file__, 'demo.blend')
if tenon.inblender():
    main()

# Define a scene first, then apply scene spefic operation.
