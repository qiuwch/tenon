# Script to change clothes of makehuman model.
import glob
import logging
import os
from tenon.config import bpyPathHelper

class Cloth:
	textures = []

	@classmethod
	def setFolder(cls, folder):
		folder = bpyPathHelper(folder)
		jpgs = glob.glob('%s/*.jpg' % folder)
		pngs = glob.glob('%s/*.png' % folder)

		cls.textures = jpgs + pngs
		logging.info('Cloth folder is set to %s, num: %d' % (folder, len(cls.textures)))

	@classmethod
	def changeByFilename(cls, filename):
		if not os.path.isfile(filename):
			logging.error('Background is set to a non-exsiting file %s' % filename)

		textureKey = cls.getTextureKey()
		import bpy
		textureImg = bpy.data.images[textureKey]
		textureImg.filepath = bpy.path.relpath(filename)

	@classmethod
	def changeById(cls, id):
		''' Change clothes by given id '''
		if id < 0 or id > (len(cls.textures) - 1):
			logging.error('Try changing pants to id %d, but index out of range' % id)
		else:
			filename = cls.textures[id]
			cls.changeByFilename(filename)

	@classmethod
	def getTextureKey(cls):
		import bpy
		# Check which one exists
		isValid = [bpy.data.images.get(k) != None for k in cls.textureKeys]

		if not True in isValid:
			logging.error('Can not find a suitable key for pants')
			return None
		else:
			index = isValid.index(True)
			return cls.textureKeys[index]



class Pants(Cloth):
	textureKeys = ['jeans_basic_diffuse.png', 'short01_black_diffuse.png', 'worksuit_diffuse.png']

	@classmethod
	def setTestingFolder(cls):
		cls.setFolder('//textures/cloth/upper/')

class TShirt(Cloth):
	textureKeys = ['tshirt02_texture.png']

	@classmethod
	def setTestingFolder(cls):
		cls.setFolder('//textures/cloth/lower/')

