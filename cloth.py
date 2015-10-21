# Script to change clothes of makehuman model.
import glob
from tenon.config import bpyPathHelper

class ClothType:
	Jeans, TShirt, LongTShirt, Shirt, Short = range(5)

textureConfig = {
	ClothType.TShirt: 'tshirt02_texture.png',
	ClothType.Jeans: 'jeans_basic_diffuse.png',
	ClothType.Short: 'short01_black_diffuse.png'
};

clothTextures = []
pantTextures = []

def setClothFolder(clothFolder):
	global clothTextures

	clothFolder = bpyPathHelper(clothFolder)
	jpgs = glob.glob('%s/*.jpg' % clothFolder)
	pngs = glob.glob('%s/*.png' % clothFolder)

	clothTextures = jpgs + pngs
	print('Cloth folder is set to %s, num: %d' % (clothFolder, len(clothTextures)))

def setPantFolder(pantFolder):
	global pantTextures

	pantFolder = bpyPathHelper(pantFolder)
	jpgs = glob.glob('%s/*.jpg' % pantFolder)
	pngs = glob.glob('%s/*.png' % pantFolder)

	pantTextures = jpgs + pngs
	print('Cloth folder is set to %s, num: %d' % (pantFolder, len(pantTextures)))


def changeClothById(clothType, id):
	global clothTextures
	global pantTextures
	if clothType == ClothType.TShirt or clothType == ClothType.LongTShirt:
		textures = clothTextures

	if clothType == ClothType.Short or clothType == ClothType.Jeans:
		textures = pantTextures

	''' Change clothes by given id '''
	if id < 0 or id > (len(textures) - 1):
		print('Index out of range')
	else:
		filename = textures[id]
		changeClothByFilename(clothType, filename)


def changeClothByFilename(clothType, filename):
	import bpy
	textureImg = bpy.data.images[textureConfig[clothType]]
	textureImg.filepath = bpy.path.relpath(filename)
