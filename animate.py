import bpy
from tenon.skeleton import world2camera
from tenon.config import selectedBones

def toFrame(frameId):
	""" Set the frame id of the scene """
	# The commented snippets below is not working
	# bpy.context.scene.frame_current = frameId
	# bpy.context.scene.update() # Update the frame index first

	bpy.context.scene.frame_set(frameId)
	obj = bpy.data.objects['human_model']

	joints = [] # Return joint position of this frame

	for bone in selectedBones:
		boneName = bone[0]
		tailOrHead = bone[1]

		bone = obj.pose.bones[boneName]
		poseBone = bone

		if tailOrHead == 'head':
			jointLocation = poseBone.head
		elif tailOrHead == 'tail':
			jointLocation = poseBone.tail

		joints.append(world2camera(jointLocation))

	return joints		
