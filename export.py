import bpy
# from skeleton import selectedBones

exportBones = {
    'shin.fk.L': 'head',
    'shin.fk.R': 'head',
    'thigh.fk.L': 'head',
    'thigh.fk.R': 'head',
    'head': 'tail',
    'foot.fk.L': 'head',
    'foot.fk.R': 'head',
    'hand.fk.L': 'head',
    'hand.fk.R': 'head',
    'forearm.fk.R': 'head',
    'forearm.fk.L': 'head',
    # 'deltoid.L': 'head',
    # 'deltoid.R': 'head',
    'upper_arm.fk.L': 'head',
    'upper_arm.fk.R': 'head',
    'neck': 'head'
}

def export_3d_joints():
	""" Export the joint 3d locations to a text file """
	obj = bpy.data.objects['human_model']

	f = open('/q/cache/joints.txt', 'w')
	for bone in obj.pose.bones:
		if not bone.name in exportBones.keys():
			continue

		jointType = exportBones[bone.name]
		if jointType == 'head':
			location = bone.head
		elif jointType == 'tail':
			location = bone.tail

		print(bone.name, location)
		# f.write(bone.name + location.__str__() + '\n')
		f.write(bone.name + ' ' + str(location.x) + ' ' + str(location.y) + ' ' + str(location.z) + '\n')
	f.close()

