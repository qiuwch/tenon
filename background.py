'''Change background of scene
'''

import bpy
import glob

INRIA_DIR = '/Users/qiuwch/Dropbox/Workspace/CG/rendering/background/INRIA/'
INRIA_SIZE = len(glob.glob(INRIA_DIR + '*.jpg'))

def setBackground(filename):
	""" Set background of the scene"""
	realpath = bpy.path.abspath(filename)
	img = bpy.data.images.load(realpath); 
	# bpy.data.images['Beautiful-Garden-HD-Wallpapers.jpg'];
	bpy.data.textures['bg'].image = img;


def setINRIA(id):
	""" Set background with INRIA dataset """
	files = glob.glob(INRIA_DIR + '*.jpg')
	setBackground(files[id])
