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

def realisticMode():
	render.realisticMode()

def demo():
	len = bpy.context.scene.frame_end
	combo = [[fid, bid] for fid in range(len) for bid in range(2)]

	for (fid, bid) in combo:
	# setCamPos(0)
		background.setINRIA(bid)

		animate.toFrame(fid); 
		prefix = 'f%d_b%d' % (fid, bid)
		render.renderFrame(prefix)

def setup():
	skeleton.createMarker()

