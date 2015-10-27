# Change background of scene
# TODO: consider merge this with scene.py
import glob
from tenon.config import bpyPathHelper

def changeBGbyFilename(filename):
	import bpy
	""" Set background of the scene"""
	abspath = bpy.path.abspath(filename)
	basename = bpy.path.basename(abspath)
	img = bpy.data.images.get(basename)
	if img == None:
		img = bpy.data.images.load(abspath); 
	bpy.data.textures['bg'].image = img

bgFiles = []

def setBGFolder(bgFolder):
	global bgFiles

	bgFolder = bpyPathHelper(bgFolder)
	jpgs = glob.glob('%s/*.jpg' % bgFolder)
	pngs = glob.glob('%s/*.png' % bgFolder)

	bgFiles = jpgs + pngs
	print('Background folder is set to %s, num: %d' % (bgFolder, len(bgFiles)))

def changeBGbyId(id):
	global bgFiles

	""" Set background with INRIA dataset """
	filename = bgFiles[id]
	print('Set background to %s' % filename)
	changeBGbyFilename(filename)
