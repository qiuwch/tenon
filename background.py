# Change background of scene

import bpy
import glob
from tenon.config import INRIA_DIR

INRIA_SIZE = len(glob.glob(INRIA_DIR + '*.jpg'))

def setBackground(filename):
	""" Set background of the scene"""
	abspath = bpy.path.abspath(filename)
	img = bpy.data.images.load(abspath); 
	bpy.data.textures['bg'].image = img;


def setINRIA(id):
	""" Set background with INRIA dataset """
	files = glob.glob(INRIA_DIR + '*.jpg')
	setBackground(files[id])
