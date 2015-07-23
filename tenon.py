'''
exec(compile(open(filename).read(), filename, 'exec'))
/Users/qiuwch/Dropbox/Workspace/CG/rendering/tenon/tenon.py
'''
import sys
sys.path.append('/Users/qiuwch/Dropbox/Workspace/CG/rendering/tenon/')
if "camera" in locals():
	import imp
	imp.reload(camera)
	imp.reload(skeleton)
	imp.reload(background)
	imp.reload(animate)
	imp.reload(render)
else:
	import camera
	import skeleton
	import background
	import animate
	import render
	import bpy

# Add support for reload

def setup():
	skeleton.createMarker()

#--------------------
# Testing / debugging
#--------------------
def renderNatural():
	render.realistic()

def renderBoundary():
	render.boundary()

def renderJoint():
	render.joints()


def main():
	# for frameId in range(bpy.context.scene.frame_end):
	for frameId in range(20):
		animate._updateJointBall()
		animate.flush()

		animate.updateJointMarker()
		print('Joint location is updated')

		for theta in [0, 90, 180, 270]:
			setCamPos(theta)
			# Change to a new setting
			# Set camera position
			snapshot('f%d_loc%d' % (frameId, theta))

			# Set frame location

			# Invoke render
