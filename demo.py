''' Include common tasks provided in tenon '''
from tenon.render import render
import bpy
import tenon.background
import tenon.animate
import tenon.skeleton
from tenon.skeleton import selectedBones
from tenon.config import JOINT_FILENAME

# TODO: Add support for reload

version = 'v2'

def realisticMode():
	''' Set the render to realistic mode '''
	render.realisticMode()

def batchRender(num):
	''' Render number of frames '''
	infoFilename = render.outputFolder + '/info.csv'
	jointFilename = JOINT_FILENAME
	fInfo = open(infoFilename, 'w')
	fJoint = open(jointFilename, 'w')

	finfoTitle = 'ImageId, finImgame, frameId, background'
	fInfo.write(finfoTitle + '\n')
	keys = []
	for v in selectedBones.keys():
		keys += [v + '.x', v + '.y'] # x, y coordinates for this joint

	jointTitle = 'ImageId,' + ','.join(keys) # No space is allowed
	fJoint.write(jointTitle + '\n') # Todo, add the id of joints

	# TODO: make verbose output fresh during execution?
	nImg = min(num, bpy.context.scene.frame_end)

	bid = 1 # bid is background id, should be randomly chosen
	print('Generating image')


	# seq = range(0, 200, 5)
	seq = range(0, 250)
	seq = seq[0:nImg]

	for ii in range(len(seq)):
		fid = seq[ii]
		# fid is frame id
		# setCamPos(0)
		tenon.background.setINRIA(bid)

		joints = tenon.animate.toFrame(fid);
		prefix = 'im%04d' % (ii+1) # Let it start from 1

		render.realisticMode()
		render.write('/imgs/' + prefix + '.png')

		render.depthMode()
		render.write('/depth/' + prefix + '.png')

		# Disabled
		# render.boundaryMode()
		# render.write('/edge/' + prefix + '.png')

		# Write file information
		fileinfo = '%04d,%s,%d,%d' % (ii, prefix, fid, bid)
		fInfo.write(fileinfo + '\n')

		# Write PC joint annotation
		b = []
		for j in joints:
			b = b + list(j)
		jointinfo = ','.join(map(str, b))
		jointinfo = '%04d,' % ii + jointinfo
		fJoint.write(jointinfo + '\n')


	fInfo.close()
	fJoint.close()


def setupSkeleton():
	tenon.skeleton.createMarker()

