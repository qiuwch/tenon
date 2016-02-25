# Demo script to show how to generate random lighting
import os, sys
tenonpath = os.path.abspath('..')
sys.path.append(tenonpath) # Install tenon
import tenon

rootdir = './../../'
def main():
    import tenon.logging as L
    L.setLevel(L.DEBUG)
    cachedir = os.path.abspath(os.path.join(rootdir, 'cache/examples/render_mode'))

    tenon.render.write(os.path.join(cachedir, 'normal_mode.png'))

    tenon.render.DepthMode.enable()
    tenon.render.write(os.path.join(cachedir, 'depth_mode.png'))
    tenon.render.DepthMode.disable()

    tenon.render.PaintMode.enable(tenon.obj.get('Suzanne'))
    tenon.render.write(os.path.join(cachedir, 'paint_mode.png'))

if not tenon.inblender():
    tenon.run(__file__, '../demo.blend')
else:
    main()
