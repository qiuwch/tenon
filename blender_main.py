'''
filename = '/Users/qiuwch/Dropbox/Workspace/CG/blender/script/blender_main.py'
exec(compile(open(filename).read(), filename, 'exec'))
'''


import bpy
import mathutils
import os

class ArmatureToMesh():
	"""Armature to mesh/skin conversion script"""
	bl_idname = "object.armature_to_mesh_skin"
	bl_label = "Armature to Mesh/Skin"
	bl_options = {'REGISTER', 'UNDO'}

	def decomposeMatrix(self, matrix):
		return [x.to_3d() for x in matrix.transposed()]

	def processArmature(self, context, arm, genVertexGroups = True):
		# arm is armature
		print("processing armature {0}".format(arm.name))

		if genVertexGroups:
			#because setting pose_position ot 'REST' manually doesn't work for some reason.
			genVertexGroups = arm.data.pose_position == 'REST'

		meshName = arm.name + "_mesh"

		# human_model_mesh, delete this first
		existMesh = context.scene.objects.get(meshName)
		if existMesh:
			context.scene.objects.unlink(existMesh)

		existObj = bpy.data.objects.get(meshName)
		if existObj:
			bpy.data.objects.remove(existObj)

		meshData = bpy.data.meshes.new(meshName + "Data")
		meshObj = bpy.data.objects.new(meshName, meshData)
		meshObj.location = arm.location

		scene = context.scene
		scene.objects.link(meshObj)

		armMatrix = arm.matrix_local.copy()

		verts = []
		edges = []
		faces = []
		vertexGroups = {}

		selectedBones = [
		'head',
		'chest',
		'neck',
		'hand.R',
		'hand.L',
		'ankle.L',
		'ankle.R',
		'elbow.link.R',
		'elbow.link.L',
		'hipside.L',
		'hipside.R',
		'knee.link.R',
		'knee.link.L'
		]

		for bone in arm.pose.bones:
			poseBone = bone
			boneName = bone.name
			armBone = arm.data.bones[boneName]
			#print(poseBone.matrix)
			#print(armBone.matrix)
			# print(boneName)

			if not boneName in selectedBones:
				continue

			boneMatrix = poseBone.matrix
			boneStart = poseBone.head
			boneEnd = poseBone.tail

			decomposedMatrix = self.decomposeMatrix(boneMatrix)
			#print(decomposedMatrix)
			xSize = armBone.bbone_x
			zSize = armBone.bbone_z
			#print(xSize, zSize)
			xSizeAdd = bone.x_axis
			zSizeAdd = bone.z_axis
			xSizeAdd = decomposedMatrix[0]
			zSizeAdd = decomposedMatrix[2]
			ySizeAdd = decomposedMatrix[1]
			origin = mathutils.Vector((0.0, 0.0, 0.0)) * boneMatrix
			xSizeAdd *= xSize
			zSizeAdd *= zSize
			ySizeAdd *= bone.length

			baseIndex = len(verts)

			verts.append((boneStart - xSizeAdd + zSizeAdd)*armMatrix)
			verts.append((boneStart + xSizeAdd + zSizeAdd)*armMatrix)
			verts.append((boneStart - xSizeAdd - zSizeAdd)*armMatrix)
			verts.append((boneStart + xSizeAdd - zSizeAdd)*armMatrix)
			verts.append((boneEnd - xSizeAdd + zSizeAdd)*armMatrix)
			verts.append((boneEnd + xSizeAdd + zSizeAdd)*armMatrix)
			verts.append((boneEnd - xSizeAdd - zSizeAdd)*armMatrix)
			verts.append((boneEnd + xSizeAdd - zSizeAdd)*armMatrix)

			base = baseIndex
			newFaces = [
				(base+0, base+1, base+3, base+2),
				(base+5, base+4, base+6, base+7),
				(base+1, base+0, base+4, base+5),
				(base+2, base+3, base+7, base+6),
				(base+3, base+1, base+5, base+7),
				(base+0, base+2, base+6, base+4)
				]
			faces.extend(newFaces)

			if genVertexGroups:
				vertexGroups[boneName] = [(x, 1.0) for x in range(baseIndex, len(verts))]

		meshData.from_pydata(verts, edges, faces) # Check API for this function

		if genVertexGroups:
			for name, vertexGroup in vertexGroups.items():
				groupObject = meshObj.vertex_groups.new(name)
				for (index, weight) in vertexGroup:
					groupObject.add([index], weight, 'REPLACE')

			modifier = meshObj.modifiers.new('ArmatureMod', 'ARMATURE')
			modifier.object = arm
			modifier.use_bone_envelopes = False
			modifier.use_vertex_groups = True

		meshData.update()

		return meshObj

	def processObject(self, context, obj):
		if (obj == None):
			return False
		if (obj.type != "ARMATURE"):
			print ("invalid type {0} of object {1}: armature expected".format(obj.type, obj.name))
			return False
		self.processArmature(context, obj)
		return True

	def execute(self, context):
			scene = context.scene
			selected = context.selected_objects
			processedAnything = False
			if len(selected) > 0:
				print ("selected objects present, processing selection")
				for obj in selected:
					processedAnything |= self.processObject(context, obj)
				pass
			else:
				print ("processing active object")
				obj = context.active_object
				processedAnything |= self.processObject(context, obj)

			if not processedAnything:
				print ("no objects processed")

			return {'FINISHED'}

def convertArmature():
	cov = ArmatureToMesh()
	cov.execute(bpy.context)


'''
Manual step. Change the freestyle type, only check contour and uncheck others
'''
def _freestyle():
	bpy.data.scenes['Scene'].render.use_freestyle = True
	# bpy.context.scene.select_crease = False
	# TODO

	layers = bpy.data.scenes['Scene'].render.layers['RenderLayer']
	layers.use_solid = False
	layers.use_halo = False
	layers.use_ztransp = False
	layers.use_sky = False
	layers.use_edge_enhance = False
	layers.use_strand = False
	
	layers.use_freestyle = True

def _realistic():
	layers = bpy.data.scenes['Scene'].render.layers['RenderLayer']
	layers.use_ztransp = True
	layers.use_freestyle = False
	layers.use_solid = True


def _activeHuman():
	for i in range(10):
		bpy.data.scenes['Scene'].layers[i] = False
		bpy.data.scenes['Scene'].render.layers['RenderLayer'].layers[i] = False

	for i in [0, 2]:
		bpy.data.scenes['Scene'].layers[i] = True
		bpy.data.scenes['Scene'].render.layers['RenderLayer'].layers[i] = True

def _activeSkeleton():
	for i in range(10):
		bpy.data.scenes['Scene'].layers[i] = False
		bpy.data.scenes['Scene'].render.layers['RenderLayer'].layers[i] = False

	for i in [3]:
		bpy.data.scenes['Scene'].layers[i] = True
		bpy.data.scenes['Scene'].render.layers['RenderLayer'].layers[i] = True

def _render(filename):
	# TOOD how to get blender directory
	# renderDir = '//output/' + 'camera' + conf['campos'] + '/'
	renderDir = '/Users/qiuwch/Dropbox/Workspace/CG/blender/human/test_scene/output/' + 'camera' + conf['campos'] + '/' 
	if not os.path.exists(renderDir):
		os.mkdir(renderDir)
	bpy.data.scenes['Scene'].render.filepath = renderDir + filename
	bpy.ops.render.render(write_still=True)




def _setCameraConstraint():
	# Deselect all objects
	bpy.ops.object.select_all(action='DESELECT')

	# Select camera
	conf['obj'].select = True
	conf['camobj'].select = True


	# Make the object active
	bpy.context.scene.objects.active = conf['obj']

	# Set tracking constraint
	bpy.ops.object.track_set()

def initCamera():
	_setCameraConstraint()
	conf['camInited'] = True



conf = {}

def main():
	conf['obj'] = bpy.data.objects.get('Cube')
	if not conf['obj']:
		print('No selected obj')

	conf['camobj'] = bpy.data.objects.get('Camera')
	if not conf['camobj']:
		print('No camera')

	conf['camInited'] = False
	initCamera()

	for theta in range(0, 360, 90):
		setCamPos(theta)
		boundary()
		realistic()

