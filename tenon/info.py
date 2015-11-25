# Retrieve the information of the scene, rendering, etc.
# These information should be stored for debugging or reproducible

import bpy
def cameraInfo():
	cam = bpy.data.objects['Camera']
	infoTemplate = \
'''Camera name: %(name)s,
Location: %(x).2f, %(y).2f, %(z).2f
'''

	infoStr = infoTemplate % {
		'name': cam.name,
		'x': cam.location.x,
		'y': cam.location.y,
		'z': cam.location.z
	}

	return infoStr

def blendInfo():
	infoTemplate = \
'''Blend file: %(blendFile)s
'''

	infoStr = infoTemplate % {
		'blendFile': bpy.data.filepath
	}

	return infoStr

class Logger():
	def __init__(self, logFile):
		self.log = open(logFile, 'w')

	def __del__(self):
		self.log.close()

	def info(self, msg):
		self.log.write(msg)
		print(msg)

