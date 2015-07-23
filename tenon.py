'''
exec(compile(open(filename).read(), filename, 'exec'))
/Users/qiuwch/Dropbox/Workspace/CG/rendering/tenon/tenon.py
'''
import sys
sys.path.append('/Users/qiuwch/Dropbox/Workspace/CG/rendering/tenon/')
if "camera" in locals():
	import imp
	imp.reload(camera)
	imp.reload(skeleton)
	imp.reload(background)
	imp.reload(animate)
	imp.reload(_render)
else:
	import camera
	import skeleton
	import background
	import animate
	import _render
	import bpy

# Add support for reload
render = _render.Render()
render.setOutputFolder('/Users/qiuwch/Downloads/renderOutput/')


def demo():
	setCamPos(0)
	len = bpy.context.scene.frame_end
	for id in range(len):
		print('%d/%d' % (id, len))
		animate.toFrame(id); render.renderFrame(id)

def setup():
	skeleton.createMarker()

