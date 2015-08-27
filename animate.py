import bpy
from tenon.skeleton import selectedBones


def toFrame(frameId):
	"""
	Set the frame id of the scene
	"""
	# This way of set frame id is not working
	# bpy.context.scene.frame_current = frameId
	# bpy.context.scene.update() # Update the frame index first

	bpy.context.scene.frame_set(frameId)
	obj = bpy.data.objects['human_model']

	for bone in obj.pose.bones:
	    if not bone.name in selectedBones.keys():
	        continue

	    poseBone = bone

	    objName = bone.name + 'Ball'
	    ball = bpy.data.objects[objName]
	    ball.location = poseBone.head
	    
	# bpy.ops.anim.change_frame(frameId)
	# for frameId in range(bpy.context.scene.frame_end):


