from tenon.core import Models
# This script can generate detailed human part labeling.
# Paint the model first

body = Models.bodyMesh()
jeans = Models.lowerCloth()
short = Models.lowerCloth()
hair = Models.hair()
tshirt = Models.upperCloth()

def humanPaintOn():
	for v in [body, jeans, hair, tshirt, short]:
		paintModeOn(v)

def humanPaintOff():
	for v in [body, jeans, hair, tshirt, short]:
		paintModeOff(v)

def paintModeOn(obj):
	''' Switch the render to paint mode '''
	if obj:
		for slot in obj.material_slots:
			_materialOn(slot.material)

def paintModeOff(obj):
	''' Disable Paint Mode, reverse previous operation '''	
	if obj:
		for slot in obj.material_slots:
			_materialOff(slot.material)

def _materialOn(material):
	if material:
		material.use_shadeless = True
		material.use_vertex_color_paint = True

		material.use_transparency = False
		for i in range(len(material.use_textures)): 
			material.use_textures[i] = False

def _materialOff(material):
	if material:
		material.use_shadeless = False
		material.use_vertex_color_paint = False

		material.use_transparency = True
		for i in range(len(material.use_textures)): 
			material.use_textures[i] = True




