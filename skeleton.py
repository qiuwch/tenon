'''
Create mesh for skeleton generation
exec(compile(open(filename).read(), filename, 'exec'))
'''

# Create an UV sphere for each joint, then assign the material to the joints.
obj = bpy.data.objects['human_model']

# selectedBones = {
# 	'head': [0, 0, 1],
# 	'chest': [0, 1, 0],
# 	'neck': [0, 1, 1],
# 	'hand.R': [1, 0, 0],
# 	'hand.L': [1, 0, 1],
# 	'ankle.L': [1, 1, 0],
# 	'ankle.R': [1, 1, 1],
# 	'elbow.link.R': [0, 0, 0.5],
# 	'elbow.link.L': [0, 0.5, 0],
# 	'hipside.L': [0, 0.5, 0.5],
# 	'hipside.R': [0.5, 0, 0],
# 	'knee.link.R': [0.5, 0, 0.5],
# 	'knee.link.L': [0.5, 0.5, 0]
# }
selectedBones = {
	'shin.fk.L': [0, 0, 1],
	'shin.fk.R': [0, 1, 0],
	'thigh.fk.L': [0, 1, 1],
	'thigh.fk.R': [1, 0, 0],
	'head': [1, 0, 1],
	'foot.fk.L': [1, 1, 0],
	'foot.fk.R': [0, 0, 0],
	'hand.fk.L': [0, 0, 1],
	'hand.fk.R': [0, 1, 0],
	'forearm.fk.R': [0, 1, 1],
	'forearm.fk.L': [1, 0, 0],
	'upper_arm.fk.L': [1, 0, 1],
	'upper_arm.fk.R': [1, 1, 0],
	'neck': [0, 0, 0]
}


for bone in obj.pose.bones:
    if not bone.name in selectedBones.keys():
        continue

    poseBone = bone
    boneName = bone.name
    armBone = obj.data.bones[boneName]

    location = poseBone.head
    layers = [False for i in range(20)]
    layers[3] = True # layer 4
    bpy.ops.mesh.primitive_uv_sphere_add(size=0.2, location=location, layers=layers) # set the layers of these balls
    objName = bone.name + 'Ball'
    ball = bpy.context.active_object
    ball.name = objName

    # Add material for rendering.
    mat = bpy.data.materials.new(name = bone.name + 'Material')
    mat.use_shadeless = True
    if len(ball.data.materials):
    	ball.data.materials[0] = mat
    else:
    	ball.data.materials.append(mat)
    mat.diffuse_color = selectedBones[bone.name]
