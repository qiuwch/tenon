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
	infoFilename = render.outputFolder + '/info.csv'
	fInfo = open(infoFilename, 'w')
	# TODO: make verbose output fresh during execution?
	nImg = min(num, bpy.context.scene.frame_end)

	bid = 1 # bid is background id, should be randomly chosen
	print('Generating image')

	fInfo.write('imageId, finImgame, frameId, background\n')
	seq = range(0, 200, 5)
	seq = seq[0:nImg]
	for ii in range(len(seq)):
		fid = seq[ii]
		# fid is frame id
		# setCamPos(0)
		tenon.background.setINRIA(bid)

		tenon.animate.toFrame(fid); 
		# prefix = 'f%d_b%d' % (fid, bid)
		prefix = '%04d' % ii
		fInfo.write('%04d, %s, %d, %d\n' % (ii, prefix, fid, bid))

		# prefix = str(prefix)

		render.realisticMode()
		render.write('/imgs/' + prefix + '.png')

		render.boundaryMode()
		render.write('/mask/' + prefix + '.png')
		
		render.jointsMode()
		render.write('/skel/' + prefix + '.png')

	fInfo.close()


def setupSkeleton():
	tenon.skeleton.createMarker()

