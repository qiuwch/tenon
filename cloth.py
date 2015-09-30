# Script to change clothes of makehuman model.
import bpy
import glob

class ClothType:
	Jeans, TShirt, LongTShirt, Shirt = range(4)

textureConfig = {
	ClothType.TShirt: 'tshirt02_texture.png',
	ClothType.Jeans: 'jeans_basic_diffuse.png',
};

def changeClothById(clothType, id):
	''' Change clothes by given id '''
	jpgs = glob.glob(bpy.path.abspath('//textures/*.jpg'))
	pngs = glob.glob(bpy.path.abspath('//textures/*.png'))
	files = jpgs + pngs
	files = [bpy.path.relpath(v) for v in files]
	if id < 0 or id > (len(files) - 1):
		print('Index out of range')
	else:
		filename = files[id]
		changeClothByFilename(clothType, filename)


def changeClothByFilename(clothType, filename):
	textureImg = bpy.data.images[textureConfig[clothType]]
	textureImg.filepath = filename
