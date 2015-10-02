# Change background of scene

import bpy
import glob
from tenon.config import INRIA_DIR

def setBackground(filename):
	""" Set background of the scene"""
	abspath = bpy.path.abspath(filename)
	basename = bpy.path.basename(abspath)
	img = bpy.data.images.get(basename)
	if img == None:
		img = bpy.data.images.load(abspath); 
	bpy.data.textures['bg'].image = img


def INRIAfileList():
	INRIAfiles = glob.glob(bpy.path.abspath(INRIA_DIR) + '*.jpg')
    # TODO: avoid glob each time
	return INRIAfiles

def setINRIA(id):
	""" Set background with INRIA dataset """
	files = INRIAfileList()
	setBackground(files[id])
