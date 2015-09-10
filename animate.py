import bpy
from tenon.skeleton import world2camera
from tenon.config import selectedBones

# TODO, fix selected bone

def toFrame(frameId):
	"""
	Set the frame id of the scene
	"""
	# This way of set frame id is not working
	# bpy.context.scene.frame_current = frameId
	# bpy.context.scene.update() # Update the frame index first

	bpy.context.scene.frame_set(frameId)
	obj = bpy.data.objects['human_model']
	# joints = {}
	joints = []

	# for bone in obj.pose.bones:
	#	if not bone.name in selectedBones.keys():
	#         continue
	for bone in selectedBones:
		boneName = bone[0]
		tailOrHead = bone[1]

		bone = obj.pose.bones[boneName]

		poseBone = bone

		# objName = bone.name + 'Ball'
		# ball = bpy.data.objects[objName]

		# ball.location = poseBone.head
		# joints[bone.name] = world2camera(poseBone.head)
		if tailOrHead == 'head':
			jointLocation = poseBone.head
		elif tailOrHead == 'tail':
			jointLocation = poseBone.tail

		joints.append(world2camera(jointLocation))


	return joints		
	# bpy.ops.anim.change_frame(frameId)
	# for frameId in range(bpy.context.scene.frame_end):


