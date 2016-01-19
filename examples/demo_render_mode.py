# Demo script to show how to generate random lighting
tenonpath = '/q/workspace/tenon'
import sys; sys.path.append(tenonpath) # Install tenon
import tenon

def main():
    tenon.render.DepthMode.enable()    
    tenon.render.write('depth_mode.png')
    tenon.render.DepthMode.disable()
    tenon.render.write('normal_mode.png')
    tenon.render.PaintMode.enable(tenon.obj.get('Suzanne'))
    tenon.render.write('paint_mode.png')

tenon.run(__file__, '../demo.blend')
if tenon.inblender():
    main()
