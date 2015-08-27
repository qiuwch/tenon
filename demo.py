''' Include common tasks provided in tenon '''
from tenon.render import render
import bpy
import tenon.background
import tenon.animate
import tenon.skeleton

# Add support for reload

version = 'v2'

def realisticMode():
	''' Set the render to realistic mode '''
	render.realisticMode()

def batchRender(num):
	''' Render number of frames '''
	# TODO: make verbose output fresh during execution?
	len = min(num, bpy.context.scene.frame_end)

	bid = 1 # bid is background id, should be randomly chosen
	print('Generating image')
	for fid in range(len):
		# fid is frame id
		# setCamPos(0)
		tenon.background.setINRIA(bid)

		tenon.animate.toFrame(fid); 
		prefix = 'f%d_b%d' % (fid, bid)
		# prefix = str(prefix)
		# render current frames to image
		# output to files

		render.realisticMode()
		filename = prefix + '-real.png'
		render.write(filename)
		print(bpy.path.abspath(filename))

		render.boundaryMode()
		render.write(prefix + '-edge.png')
		render.jointsMode()
		render.write(prefix + '-joint.png')


def setupSkeleton():
	tenon.skeleton.createMarker()

