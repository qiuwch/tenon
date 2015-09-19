import bpy
import glob
# Script to change clothes of makehuman model.

class ClothType:
	Jeans, TShirt, LongTShirt, Shirt = range(4)

textureConfig = {
	ClothType.TShirt: 'tshirt02_texture.png',
	ClothType.Jeans: 'jeans_basic_diffuse.png',
};

def changeClothById(clothType, id):
	''' Change clothes by given id '''
	files = glob.glob(bpy.path.abspath('//textures/*.jpg'))
	files = [bpy.path.relpath(v) for v in files]
	if id < 0 or id > (len(files) - 1):
		print('Index out of range')
	else:
		filename = files[id]
		changeClothByFilename(clothType, filename)


def changeClothByFilename(clothType, filename):
	textureImg = bpy.data.images[textureConfig[clothType]]
	# tshirt = bpy.data.objects['human_model:tshirt02']
	# tshirt.material_slots['human_model:tshirt02:tshirt02Material']

	textureImg.filepath = filename
