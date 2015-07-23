'''Change background of scene
'''

import bpy
import glob

INRIA_DIR = '/Users/qiuwch/Dropbox/Workspace/CG/rendering/background/INRIA/'

def setBackground(filename):
	realpath = bpy.path.abspath(filename)
	img = bpy.data.images.load(realpath); 
	# bpy.data.images['Beautiful-Garden-HD-Wallpapers.jpg'];
	bpy.data.textures['bg'].image = img;


def INRIA_BG(id):
	files = glob.glob(INRIA_DIR + '*.jpg')
	setBackground(files[id])
