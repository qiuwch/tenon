
def sceneCamera():
	cam = bpy.data.objects.get('Camera')
	if not cam:
		print('No camera')
	return cam


def setCamPos(theta):
	# Change the camera position directly
	import math
	theta_rad = theta / 180.0 * math.pi

	loc1 = sceneCamera().location
	radius = math.sqrt(loc1.x ** 2 + loc1.y ** 2)

	x = math.sin(theta_rad) * radius
	y = - math.cos(theta_rad) * radius

	z = sceneCamera().location.z
	sceneCamera().location = (x, y, z)
