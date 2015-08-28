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

	def boundaryMode(self):
		''' Only display boundary of the object '''
		self._switchFreestyle(True)

		self._layersOff()
		for i in range(3):
			self.sceneLayers[i] = True
			self.renderLayers[i] = True

	def realisticMode(self):
		''' Display the realistic rendering '''
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
		self._switchFreestyle(False)

		self._offAllOption()
		self.renderLayer.use_solid = True

		self._layersOff()
		self.sceneLayers[3] = True
		self.renderLayers[3] = True

	def write(self, filename):
		if not os.path.exists(self.outputFolder):
			os.mkdir(self.outputFolder)

		self.scene.render.filepath = self.outputFolder + filename
		bpy.ops.render.render(write_still=True)

	def renderFrame(self, prefix):
		''' Render foreground region, joint location and realistic image '''
		prefix = str(prefix)
		# render current frames to image
		# output to files
		self.realisticMode()
		self.write(prefix + '-real.png')
		self.boundaryMode()
		self.write(prefix + '-edge.png')
		self.jointsMode()
		self.write(prefix + '-joint.png')

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

