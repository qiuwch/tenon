'''
filename = '/Users/qiuwch/Dropbox/Workspace/CG/blender/script/human_script.py'
exec(compile(open(filename).read(), filename, 'exec'))
'''
import os
import bpy

# design the scene

# apply freestyle setting

# setup the camera constraint

# create_ball

# Configuration section
conf = {}
conf['camobj'] = bpy.data.objects.get('Camera')
if not conf['camobj']:
	print('No camera')


def render(frameId):
	animate._updateJointBall()
	animate.flush()
	print('Joint location is updated')

	for theta in [0, 90, 180, 270]:
		camera.setCamPos(theta)
		# Change to a new setting
		# Set camera position
		snapshot('f%d_loc%d' % (frameId, theta))



# Sync this with create_ball.py
selectedBones = {
	'shin.fk.L': [0, 0, 1],
	'shin.fk.R': [0, 1, 0],
	'thigh.fk.L': [0, 1, 1],
	'thigh.fk.R': [1, 0, 0],
	'head': [1, 0, 1],
	'foot.fk.L': [1, 1, 0],
	'foot.fk.R': [1, 1, 1],
	'hand.fk.L': [0, 0, 1],
	'hand.fk.R': [0, 1, 0],
	'forearm.fk.R': [0, 1, 1],
	'forearm.fk.L': [1, 0, 0],
	'upper_arm.fk.L': [1, 0, 1],
	'upper_arm.fk.R': [1, 1, 0],
	'neck': [1, 1, 1]
}




def snapshot(prefix): # Take snapshot of the scene
	boundary()
	_render('%s_boundary.png' % prefix)

	joints()
	_render('%s_joints.png' % prefix)

	realistic()
	_render('%s_realistic.png' % prefix)

