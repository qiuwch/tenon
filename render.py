import bpy
import os
from tenon.config import RENDER_OUTPUT_DIR

class Render():
	# Options for internal render of blender
	def __init__(self):
		self.outputFolder = bpy.path.abspath(RENDER_OUTPUT_DIR)
		self.scene = bpy.data.scenes['Scene']

		# Control render config
		self.renderLayer = self.scene.render.layers['RenderLayer']

		# Control which layer is visible, TODO: what is the difference?
		self.sceneLayers = self.scene.layers
		self.renderLayers = self.scene.render.layers['RenderLayer'].layers
		self.version = 'v3'

	def setOutputFolder(self, outputFolder):
		''' Set the output folder of render '''
		self.outputFolder = bpy.path.abspath(outputFolder)

	def _switchFreestyle(self, switch):
		self.scene.render.use_freestyle = switch
		self._offAllOption()
		self.renderLayer.use_freestyle = switch


	def _enableDepth(self):
		# bpy.context.scene.use_nodes = True
		tree = bpy.context.scene.node_tree
		depthNode = tree.nodes.get('Invert')
		compositeNode = tree.nodes.get('Composite')

		links = tree.links
		links.new(depthNode.outputs[0], compositeNode.inputs[0])

	def _disableDepth(self):
		# bpy.context.scene.use_nodes = True
		tree = bpy.context.scene.node_tree
		renderLayersNode = tree.nodes.get('Render Layers')
		compositeNode = tree.nodes.get('Composite')

		links = tree.links
		links.new(renderLayersNode.outputs[0], compositeNode.inputs[0])

	def depthMode(self):
		''' Render depth of the scene. To use this function, the scene needs to be pre-configured. '''
		self.realisticMode()
		self._enableDepth()

	def boundaryMode(self):
		''' Only display boundary of the object '''
		self._disableDepth()
		self._switchFreestyle(True)

		self._layersOff()
		for i in range(3):
			self.sceneLayers[i] = True
			self.renderLayers[i] = True

	def realisticMode(self):
		''' Display the realistic rendering '''
		self._disableDepth()
		self._switchFreestyle(False)

		self._offAllOption()
		self.renderLayer.use_ztransp = True
		self.renderLayer.use_sky = True

		self._layersOff()
		for i in range(3):
			self.sceneLayers[i] = True
			self.renderLayers[i] = True

	def jointsMode(self):
		''' Only display the joint locations '''
		self._disableDepth()
		self._switchFreestyle(False)

		self._offAllOption()
		self.renderLayer.use_solid = True

		self._layersOff()
		self.sceneLayers[3] = True
		self.renderLayers[3] = True

	def write(self, filename):
		''' Write current scene to the filename '''
		if not os.path.exists(self.outputFolder):
			os.mkdir(self.outputFolder)

		# self.scene.render.filepath = self.outputFolder + filename
		self.scene.render.filepath = filename

		# TODO: improve the logging system
		print(self.scene.render.filepath)
		bpy.ops.render.render(write_still=True)

	def _offAllOption(self):
		self.renderLayer.use_zmask = False
		self.renderLayer.use_all_z = False
		self.renderLayer.use_solid = False
		self.renderLayer.use_halo = False
		self.renderLayer.use_ztransp = False
		self.renderLayer.use_sky = False
		self.renderLayer.use_edge_enhance = False
		self.renderLayer.use_strand = False
		self.renderLayer.use_freestyle = False

	def _layersOff(self):
		for i in range(20):
			self.sceneLayers[i] = False

render = Render()

