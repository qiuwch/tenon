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
pantsTextures = []

def setClothFolder(clothFolder):
	global clothTextures

	clothFolder = bpyPathHelper(clothFolder)
	jpgs = glob.glob('%s/*.jpg' % clothFolder)
	pngs = glob.glob('%s/*.png' % clothFolder)

	clothTextures = jpgs + pngs
	print('Cloth folder is set to %s, num: %d' % (clothFolder, len(clothTextures)))

def setPantsFolder(pantsFolder):
	global pantsTextures

	pantsFolder = bpyPathHelper(pantsFolder)
	jpgs = glob.glob('%s/*.jpg' % pantsFolder)
	pngs = glob.glob('%s/*.png' % pantsFolder)

	pantsTextures = jpgs + pngs
	print('Cloth folder is set to %s, num: %d' % (pantsFolder, len(pantsTextures)))


def changeClothById(clothType, id):
	global clothTextures
	global pantsTextures
	if clothType == ClothType.TShirt or clothType == ClothType.LongTShirt:
		textures = clothTextures

	if clothType == ClothType.Short or clothType == ClothType.Jeans:
		textures = pantsTextures

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
