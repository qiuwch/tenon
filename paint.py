import bpy
# This script can generate detailed human part labeling.
# Paint the model first

body = bpy.data.objects.get('human_model:Body')
jeans = bpy.data.objects.get('human_model:jeans01')
hair = bpy.data.objects.get('human_model:mhair02')
tshirt = bpy.data.objects.get('human_model:tshirt02')

def humanPaintOn():
	for v in [body, jeans, hair, tshirt]:
		paintModeOn(v)

def humanPaintOff():
	for v in [body, jeans, hair, tshirt]:
		paintModeOff(v)

def paintModeOn(obj):
	''' Switch the render to paint mode '''
	for slot in obj.material_slots:
		_materialOn(slot.material)

def paintModeOff(obj):
	''' Disable Paint Mode, reverse previous operation '''	
	for slot in obj.material_slots:
		_materialOff(slot.material)

def _materialOn(material):
	material.use_shadeless = True
	material.use_vertex_color_paint = True

	material.use_transparency = False
	for i in range(len(material.use_textures)): 
		material.use_textures[i] = False

def _materialOff(material):
	material.use_shadeless = False
	material.use_vertex_color_paint = False

	material.use_transparency = True
	for i in range(len(material.use_textures)): 
		material.use_textures[i] = True




