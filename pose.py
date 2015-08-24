import bpy
def rest():
	""" Set the human body to rest pose """

	# scn.objects.active = rig
	bpy.ops.object.mode_set(mode='POSE')
	bpy.ops.pose.select_all(action='SELECT')
	bpy.ops.pose.rot_clear()
	bpy.ops.pose.loc_clear()
	bpy.ops.pose.scale_clear()