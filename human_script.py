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
	bpy.context.scene.update()
	_updateJointBall()
	print('Joint location is updated')

	for theta in [0, 90, 180, 270]:
		setCamPos(theta)
		# Change to a new setting
		# Set camera position
		snapshot('f%d_loc%d' % (frameId, theta))


def main():
	# for frameId in range(bpy.context.scene.frame_end):
	for frameId in range(20):
		bpy.context.scene.update() 
		# This is important for the joint location to be updated

		print(frameId)
		# bpy.context.scene.frame_current = frameId
		# bpy.ops.anim.change_frame(frameId)
		_updateJointBall()
		print('Joint location is updated')

		for theta in [0, 90, 180, 270]:
			setCamPos(theta)
			# Change to a new setting
			# Set camera position
			snapshot('f%d_loc%d' % (frameId, theta))

			# Set frame location

			# Invoke render

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

def _updateJointBall():
	obj = bpy.data.objects['human_model']

	for bone in obj.pose.bones:
	    if not bone.name in selectedBones.keys():
	        continue

	    poseBone = bone

	    objName = bone.name + 'Ball'
	    ball = bpy.data.objects[objName]
	    ball.location = poseBone.head


def setCamPos(theta):
	# Change the camera position directly
	import math
	theta_rad = theta / 180.0 * math.pi

	loc1 = conf['camobj'].location
	radius = math.sqrt(loc1.x ** 2 + loc1.y ** 2)

	x = math.sin(theta_rad) * radius
	y = - math.cos(theta_rad) * radius

	z = conf['camobj'].location.z
	conf['camobj'].location = (x, y, z)

def snapshot(prefix): # Take snapshot of the scene
	boundary()
	_render('%s_boundary.png' % prefix)

	joints()
	_render('%s_joints.png' % prefix)

	realistic()
	_render('%s_realistic.png' % prefix)

def _render(filename):
	# TOOD how to get blender directory
	renderDir = '/Users/qiuwch/Downloads/render_output/'
	if not os.path.exists(renderDir):
		os.mkdir(renderDir)

	bpy.data.scenes['Scene'].render.filepath = renderDir + filename
	bpy.ops.render.render(write_still=True)

def _turnOffAll(layers):
	layers.use_zmask = False
	layers.use_all_z = False
	layers.use_solid = False
	layers.use_halo = False
	layers.use_ztransp = False
	layers.use_sky = False
	layers.use_edge_enhance = False
	layers.use_strand = False
	layers.use_freestyle = False

def _layersOff(layers):
	for i in range(20):
		layers[i] = False


def boundary():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = True

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_freestyle = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	for i in range(3):
		scene.render.layers['RenderLayer'].layers[i] = True


def realistic():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = False

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_ztransp = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	for i in range(3):
		scene.render.layers['RenderLayer'].layers[i] = True

def joints():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = False

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_solid = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	scene.render.layers['RenderLayer'].layers[3] = True
