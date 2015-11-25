import bpy

def toFrame(frameId):
	""" Set the frame id of the scene """
	# The commented snippets below is not working
	# bpy.context.scene.frame_current = frameId
	# bpy.context.scene.update() # Update the frame index first

	bpy.context.scene.frame_set(frameId)

