import bpy

def animateToFrame(frameId):
	bpy.context.scene.frame_current = frameId
	# bpy.ops.anim.change_frame(frameId)


def flush():
	bpy.context.scene.update()
	# This is important for the joint location to be updated

def updateJointMarker():
	obj = bpy.data.objects['human_model']

	for bone in obj.pose.bones:
	    if not bone.name in selectedBones.keys():
	        continue

	    poseBone = bone

	    objName = bone.name + 'Ball'
	    ball = bpy.data.objects[objName]
	    ball.location = poseBone.head
