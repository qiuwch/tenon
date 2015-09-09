''' Include common tasks provided in tenon '''
from tenon.render import render
import bpy
import tenon.background
import tenon.animate
import tenon.skeleton
from tenon.skeleton import selectedBones

# TODO: Add support for reload

version = 'v2'

def realisticMode():
	''' Set the render to realistic mode '''
	render.realisticMode()

def batchRender(num):
	''' Render number of frames '''
	infoFilename = render.outputFolder + '/info.csv'
	jointFilename = render.outputFolder + '/joint-PC.csv' # person centric annotation
	fInfo = open(infoFilename, 'w')
	fJoint = open(jointFilename, 'w')

	finfoTitle = 'ImageId, finImgame, frameId, background'
	fInfo.write(finfoTitle + '\n')
	keys = []
	for v in selectedBones.keys():
		keys += [v + '.x', v + '.y'] # x, y coordinates for this joint

	jointTitle = 'ImageId, ' + ','.join(keys)
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
		print(len(joints))

		for j in joints:
			fJoint.write(str(j[0]) + ',' + str(j[1]) + ',')
		fJoint.write('\n')
		prefix = '%04d' % ii

		print(render.version)
		render.realisticMode()
		render.write('/imgs/' + prefix + '.png')

		render.boundaryMode()
		render.write('/edge/' + prefix + '.png')
		
		render.depthMode()
		render.write('/depth/' + prefix + '.png')

		# Write file information
		fileinfo = '%04d, %s, %d, %d' % (ii, prefix, fid, bid)
		fInfo.write(fileinfo + '\n')

		# Write PC joint annotation
		b = []
		for j in joints:
			b = b + list(j)
		jointinfo = ','.join(map(str, b))
		jointinfo = '%04d, ' % ii + jointinfo
		fJoint.write(jointinfo + '\n')


	fInfo.close()
	fJoint.close()


def setupSkeleton():
	tenon.skeleton.createMarker()

