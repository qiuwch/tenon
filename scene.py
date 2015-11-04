# Utility function to check whether an operation is successful
import logging
import glob
import os
from tenon.config import bpyPathHelper
import bpy

def checkOp(ret):
	assert 'FINISHED' in ret

def roughPrintArray(arr):
	# Print the array in a not very exact way for doctest
	appArr = [round(v, 3) for v in arr]
	print(appArr)

# Why define my own data stucture for these, but this is abstraction for my problem
# This is simplified, more elegant representation
class LightSource:
	def __init__(self):
		self.location = []
		self.direction = []
		self.energy = 1
		self.name = ''

	def createBlenderLight(self):
		import mathutils

		obj = bpy.data.objects.get(self.name)
		# It seems tricky to modify the lamp name, which needs to modify lamp and obj name together

		if not obj:
			# from: http://www.blender.org/api/blender_python_api_2_66_6/bpy.types.Object.html
			# Create new lamp datablock
			scene = bpy.context.scene
			lamp_data = bpy.data.lamps.new(name=self.name, type='POINT')
			obj = bpy.data.objects.new(name=self.name, object_data=lamp_data)
			scene.objects.link(obj)

			# An alternative way
			# ret = bpy.ops.object.lamp_add(type='POINT'), Does not support name
			# checkOp(ret)

		obj.location = mathutils.Vector(self.location)
		lamp = bpy.data.lamps.get(self.name)
		logging.debug('Set lamp %s energy to %f', self.name, self.energy)
		lamp.energy = self.energy

class Lighting:
	@classmethod
	def randomCircleConfig(cls, radius=12, nLight=16, z=0):
		import random

		# Set up the light configuration
		lightConfig = []
		radius = 12
		nLight = 16
		for i in range(nLight):
			light = LightSource()

			# Compute the location of light source, put the light evenly
			light.location = cls.sphereLocation(radius, 360 / nLight * i, 0)
			light.location[2] += z  # Set the z of the light source
			light.energy = random.gauss(1, 1.5)
			light.name = 'PointLight%d' % i
			lightConfig.append(light)

		return lightConfig

	@classmethod
	def sphereLocation(cls, radius, az, el):
		''' The input of az, el should be angle, not radius
		>>> roughPrintArray(LightingConfig.sphereLocation(10, 0, 0))
		[10.0, 0.0, 0.0]
		>>> roughPrintArray(LightingConfig.sphereLocation(10, 30, 0))
		[8.66, 5.0, 0.0]
		>>> roughPrintArray(LightingConfig.sphereLocation(10, 30, 45))
		[6.124, 3.536, 7.071]
		'''
		import math
		az = math.radians(az)
		el = math.radians(el)
		z = radius * math.sin(el)
		r = radius * math.cos(el)
		x = r * math.cos(az)
		y = r * math.sin(az)
		return [x, y, z]

	@classmethod
	def setup(cls, lightConfig=None):
		if not lightConfig:
			logging.info('Create circle lighting environment')
			lightConfig = cls.randomCircleConfig(z = 1, radius = 5)

		logging.info('Create blender lights')
		for light in lightConfig:
			light.createBlenderLight()

class TextureChanger:
	textures = []

	@classmethod
	def setFolder(cls, folder):
		folder = bpyPathHelper(folder)
		jpgs = glob.glob('%s/*.jpg' % folder)
		pngs = glob.glob('%s/*.png' % folder)

		cls.textures = jpgs + pngs
		logging.info('TextureChanger folder is set to %s, num: %d' % (folder, len(cls.textures)))

	@classmethod
	def changeByFilename(cls, filename):
		if not os.path.isfile(filename):
			logging.error('Background is set to a non-exsiting file %s' % filename)

		textureKey = cls.getTextureKey()
		if not textureKey:
			logging.warning('Can not change texture for %s, no valid key' % cls.__name__)
			return

		textureImg = bpy.data.images[textureKey]
		textureImg.filepath = bpy.path.relpath(filename)

	@classmethod
	def randomChange(cls):
		import random
		N = len(cls.textures)
		if N == 0:
			logging.error('No textures available for %s' % cls.__name__)
			return

		i = random.randrange(0, N)
		filename = cls.textures[i]
		cls.changeByFilename(filename)	

	@classmethod
	def changeById(cls, id):
		''' Change clothes by given id '''
		if isinstance(id, str):
			if id.isdigit():
				id = int(id)
			else:
				logging.error('Invaid input %s to changeById' % id)

		if id < 0 or id > (len(cls.textures) - 1):
			logging.error('Try changing pants to id %d, but index out of range' % id)
		else:
			filename = cls.textures[id]
			cls.changeByFilename(filename)

	@classmethod
	def getTextureKey(cls):
		# Check which one exists
		isValid = [bpy.data.images.get(k) != None for k in cls.textureKeys]

		if not True in isValid:
			logging.error('Can not find a suitable key for %s' % cls.__name__)
			return None
		else:
			index = isValid.index(True)
			return cls.textureKeys[index]

class Pants(TextureChanger):
	textureKeys = ['jeans_basic_diffuse.png', 'short01_black_diffuse.png', 'worksuit_diffuse.png']

	@classmethod
	def setTestingFolder(cls):
		cls.setFolder('//textures/cloth/upper/')

class Shirt(TextureChanger):
	textureKeys = ['tshirt02_texture.png', 'tshirt_texture_white.png']

	@classmethod
	def setTestingFolder(cls):
		cls.setFolder('//textures/cloth/lower/')

class Hair(TextureChanger):
	textureKeys = ['male01_diffuse_black.png']

class Skin(TextureChanger):
	textureKeys = ['young_lightskinned_male_diffuse.png']

class Bg(TextureChanger):
	textureKeys = ['bg']

	@classmethod
	def setup(cls):
		textureKey = cls.textureKeys[0]
		bgTexture = bpy.data.textures.get(textureKey)
		if not bgTexture:
			logging.info('Create new background texture')
			bgTexture = bpy.data.textures.new(textureKey, type='IMAGE')
	
		bgImg = bpy.data.images.get(textureKey)
		if not bgImg:
			logging.info('Create new background image')
			bgImg = bpy.data.images.new(textureKey, width=10, height=10)

		bgImg.source = 'FILE'
		bgTexture.image = bgImg
		bpy.data.worlds['World'].active_texture = bgTexture

		# TODO: this is tricky, fix it later
		bpy.data.worlds['World'].texture_slots[0].use_map_horizon = True

	@classmethod
	def setTestingFolder(cls):
		cls.setFolder('//background/INRIA')

class Camera():
	@classmethod
	def sceneCamera(cls):
		ks = bpy.data.cameras.keys()
		cams = [bpy.data.objects.get(k) for k in ks]
		cams = [v for v in cams if v] # Remove none
		""" Return camera of the scene """
		# cam = bpy.data.objects.get('Camera')
		if len(cams) == 0:
			logging.info('No camera in the scene, create a new one')
			scene = bpy.context.scene
			cam = bpy.data.cameras.new('Camera') # The object may take a different name
			camObj = bpy.data.objects.new(name=cam.name, object_data=cam)
			scene.objects.link(camObj)
			return camObj
		else:
			return cams[0]

	@classmethod
	def setPosAngle(cls, theta):
		""" Set the position of scene camera """

		# Change the camera position directly
		import math
		theta_rad = theta / 180.0 * math.pi

		loc1 = cls.sceneCamera().location
		radius = math.sqrt(loc1.x ** 2 + loc1.y ** 2)

		x = math.sin(theta_rad) * radius
		y = - math.cos(theta_rad) * radius

		z = cls.sceneCamera().location.z
		cls.sceneCamera().location = (x, y, z)

	@classmethod
	def set(cls, loc, rot):
		cam = cls.sceneCamera()
		if not cam:
			logging.error('Can not find an active camera in the scene')			
			return

		import mathutils
		cam.location = mathutils.Vector(loc)
		cam.rotation_euler = mathutils.Euler(rot[0], rot[1])

def setupL23():
	# Setup the scene for l23 task, this can setup a default scene of blender to a working scene.
	# Minimal human labor is required

	# Setup lighting
	Lighting.setup()
	Bg.setup()

	Camera.set((0, -5, 0.7), ((1.4, 0, 0), 'XYZ'))

	# Setup pose constraint
	import tenon.puppet as pp
	pp.Constraint.setup()
	pp.animateCP(1)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    '''
    Example usage of this module
    import tenon.scene as sc
    # lightConfig  # load lighting config from a configuration file
    sc.createLighting() # if lightConfig is None, it will generate lighting randomly
    '''
