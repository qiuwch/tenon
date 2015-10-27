# Utility function to check whether an operation is successful
import logging
def checkOp(ret):
	assert 'FINISHED' in ret


# Why define my own data stucture for these, but this is abstraction for my problem
# This is simplified, more elegant representation
class LightSource:
	def __init__(self):
		self.location = []
		self.direction = []
		self.energy = 1
		self.name = ''

	def createBlenderLight(self):
		import mathutils, bpy

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


# class SceneLight: # Define the light configuration for this scene
# 	def __init__(self):
# 		self.lightConfig = [] # Contains a bunch of light sources



# 	def setupBlenderScene(self):
# 		''' Create the lighting of the scene according to its configuration
# 		Easier to start from scratch than manipulating current setting
# 		'''
# 		import bpy

# 		def clearBlenderLights():
# 			''' It is hard to write unit test for blender scripts '''
# 			lamps =  bpy.data.lamps.values()

# 			oldMode = bpy.context.mode
# 			bpy.ops.object.mode_set(mode='OBJECT')
# 			for v in lamps:
# 				bpy.data.objects[v.name].select = True
# 				bpy.ops.object.delete()
# 			bpy.ops.object.mode_set(mode=oldMode)




def roughPrintArray(arr):
	# Print the array in a not very exact way for doctest
	appArr = [round(v, 3) for v in arr]
	print(appArr)



class LightingConfig:
	@classmethod
	def randomCircleConfig(cls, z=0):
		import random

		# Set up the light configuration
		lightConfig = []
		radius = 12
		nLight = 16
		for i in range(nLight):
			light = LightSource()

			# Compute the location of light source, put the light evenly
			light.location = LightingConfig.sphereLocation(radius, 360 / nLight * i, 0)
			light.location[2] += z  # Set the z of the light source
			light.energy = random.gauss(1, 2)
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

class Lighting:
	@classmethod
	def setup(cls, lightConfig=None):
		if not lightConfig:
			logging.info('Create circle lighting environment')
			lightConfig = LightingConfig.randomCircleConfig(z = 0)

		logging.info('Create blender lights')
		for light in lightConfig:
			light.createBlenderLight()

def l23setup():
	# Setup the scene for l23 task, this can setup a default scene of blender to a working scene.
	# Minimal human labor is required

	# Setup background
	print('Setup background node')

	# Setup lighting
	Lighting.setup()

	# Setup pose constraint
	import tenon.puppet as pp
	pp.Constraint.setup()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    '''
    Example usage of this module
    import tenon.scene as sc
    # lightConfig  # load lighting config from a configuration file
    sc.createLighting() # if lightConfig is None, it will generate lighting randomly
    '''
