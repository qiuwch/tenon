import bpy

def boundary():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = True

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_freestyle = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	for i in range(3):
		scene.render.layers['RenderLayer'].layers[i] = True

def realistic():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = False

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_ztransp = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	for i in range(3):
		scene.render.layers['RenderLayer'].layers[i] = True

def joints():
	scene = bpy.data.scenes['Scene']
	scene.render.use_freestyle = False

	_turnOffAll(scene.render.layers['RenderLayer'])
	scene.render.layers['RenderLayer'].use_solid = True

	# Select the layers of joints
	_layersOff(scene.render.layers['RenderLayer'].layers)
	scene.render.layers['RenderLayer'].layers[3] = True

def _render(filename):
	# TOOD how to get blender directory
	renderDir = '/Users/qiuwch/Downloads/render_output/'
	if not os.path.exists(renderDir):
		os.mkdir(renderDir)

	bpy.data.scenes['Scene'].render.filepath = renderDir + filename
	bpy.ops.render.render(write_still=True)

def _turnOffAll(layers):
	layers.use_zmask = False
	layers.use_all_z = False
	layers.use_solid = False
	layers.use_halo = False
	layers.use_ztransp = False
	layers.use_sky = False
	layers.use_edge_enhance = False
	layers.use_strand = False
	layers.use_freestyle = False

def _layersOff(layers):
	for i in range(20):
		layers[i] = False


