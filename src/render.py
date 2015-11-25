import bpy
import tenon.paint
import tenon.config
from tenon.config import RENDER_OUTPUT_DIR
from tenon.core import Models
import logging

class Depth:
    @classmethod    
    def enable(cls):
        cls.setup()
        cls.tree.links.new(cls.renderLayersNode.outputs[2], cls.normalizeNode.inputs[0])
        cls.tree.links.new(cls.invertNode.outputs[0], cls.compositeNode.inputs[0])

    @classmethod
    def disable(cls):
        cls.setup()
        cls.tree.links.new(cls.renderLayersNode.outputs[0], cls.compositeNode.inputs[0])

    @classmethod
    def setup(cls):
        tree = bpy.context.scene.node_tree
        if not tree:
            bpy.context.scene.use_nodes = True
            tree = bpy.context.scene.node_tree

        renderLayersNode = tree.nodes.get('Render Layers')
        compositeNode = tree.nodes.get('Composite')
        
        if not renderLayersNode or not compositeNode:
            logging.error('Error in setuping up depth mode, renderLayersNode and compositeNode are missing')

        invertNode = tree.nodes.get('Invert')
        if not invertNode:
            invertNode = tree.nodes.new('CompositorNodeInvert')  # The type name is changed and undocumented
            # Check this url https://developer.blender.org/T35336

        normalizeNode = tree.nodes.get('Normalize')
        if not normalizeNode:
            normalizeNode = tree.nodes.new('CompositorNodeNormalize')

        tree.links.new(normalizeNode.outputs[0], invertNode.inputs[0])
        cls.tree = tree
        cls.renderLayersNode = renderLayersNode
        cls.compositeNode = compositeNode
        cls.invertNode = invertNode
        cls.normalizeNode = normalizeNode


class Render:
    # Options for internal render of blender
    outputFolder = bpy.path.abspath(RENDER_OUTPUT_DIR)
    scene = bpy.data.scenes['Scene']

    # Control render config
    renderLayer = scene.render.layers['RenderLayer']

    # Control which layer is visible, TODO: what is the difference?
    sceneLayers = scene.layers
    renderLayers = scene.render.layers['RenderLayer'].layers
    use_sky = True

    @classmethod
    def skyOff(cls):
        cls.use_sky = False

    @classmethod
    def skyOn(cls):
        cls.use_sky = True

    @classmethod
    def setOutputFolder(cls, outputFolder):
        ''' Set the output folder of render '''
        cls.outputFolder = bpy.path.abspath(outputFolder)

    @classmethod
    def _switchFreestyle(cls, switch):
        cls.scene.render.use_freestyle = switch
        cls._offAllOption()
        cls.renderLayer.use_freestyle = switch

    @classmethod
    def depthModeOn(cls):
        ''' Render depth of the scene. To use this function, the scene needs to be pre-configured. '''
        Depth.enable()

    @classmethod
    def depthModeOff(cls):
        Depth.disable()

    @classmethod
    def boundaryMode(cls):
        ''' Only display boundary of the object '''
        Depth.disable()
        cls._switchFreestyle(True)

        cls._layersOff()
        for i in range(3):
            cls.sceneLayers[i] = True
            cls.renderLayers[i] = True

    @classmethod
    def realisticMode(cls):
        ''' Display the realistic rendering '''
        Depth.disable()
        cls._switchFreestyle(False)

        # cls._offAllOption()
        cls.renderLayer.use_ztransp = True
        cls.renderLayer.use_sky = cls.use_sky
        cls.renderLayer.use_solid = True

        cls._layersOff()
        for i in range(3):
            cls.sceneLayers[i] = True
            cls.renderLayers[i] = True

    @classmethod
    def jointsMode(cls):
        ''' Only display the joint locations '''
        Depth.disable()
        cls._switchFreestyle(False)

        # cls._offAllOption()
        cls.renderLayer.use_solid = True

        cls._layersOff()
        cls.sceneLayers[3] = True
        cls.renderLayers[3] = True

    @classmethod
    def paintModeOn(cls):
        cls.renderLayer.use_sky = False
        tenon.paint.humanPaintOn()

    @classmethod
    def paintModeOff(cls):
        cls.renderLayer.use_sky = cls.use_sky
        tenon.paint.humanPaintOff()

    @classmethod
    def write(cls, filename):
        ''' Write current scene to the filename '''
        # TODO: check whether this location writable
        # if not os.path.exists(cls.outputFolder):
        #   os.mkdir(cls.outputFolder)

        # cls.scene.render.filepath = cls.outputFolder + filename
        cls.scene.render.filepath = filename
        cls.scene.update()

        logging.info('Render to file %s' % cls.scene.render.filepath)
        bpy.ops.render.render(write_still=True)

    @classmethod
    def exportJoint(cls):
        from tenon.skeleton import world2camera

        selectedBones = [
            # 1. name of the bone
            # 2. use tail or head location of the bone
            ('thigh.fk.L', 'tail'), # ('shin.fk.L', 'head'),
            ('thigh.fk.R', 'tail'), # easier for rotation
            ('thigh.fk.L', 'head'),
            ('thigh.fk.R', 'head'),
            ('head', 'tail'),
            ('shin.fk.L', 'tail'), # ('foot.fk.L', 'head'),
            ('shin.fk.R', 'tail'), # ('foot.fk.R', 'head'),
            ('forearm.fk.L', 'tail'), #('hand.fk.L', 'head'),
            ('forearm.fk.R', 'tail'), # ('hand.fk.R', 'head'),
            ('upper_arm.fk.L', 'tail'), # ('forearm.fk.R', 'head'),
            ('upper_arm.fk.R', 'tail'), # ('forearm.fk.L', 'head'),
            ('upper_arm.fk.L', 'head'),
            ('upper_arm.fk.R', 'head'),
            ('neck', 'head')
        ]

        obj = Models.humanModel()
        joints = [] # Return joint position of this frame
        for boneInfo in selectedBones:
            boneName = boneInfo[0]
            tailOrHead = boneInfo[1]
            poseBone = obj.pose.bones[boneName]

            if tailOrHead == 'head':
                jointLocation = poseBone.head
            elif tailOrHead == 'tail':
                jointLocation = poseBone.tail

            boneId = '%s.%s' % (boneName, tailOrHead)
            joints.append((boneId, world2camera(jointLocation)))
        return joints       

    @classmethod
    def _offAllOption(cls):
        cls.renderLayer.use_zmask = False
        cls.renderLayer.use_all_z = False
        cls.renderLayer.use_solid = False
        cls.renderLayer.use_halo = False
        cls.renderLayer.use_ztransp = False
        cls.renderLayer.use_sky = False
        cls.renderLayer.use_edge_enhance = False
        cls.renderLayer.use_strand = False
        cls.renderLayer.use_freestyle = False

    @classmethod
    def _layersOff(cls):
        for i in range(20):
            cls.sceneLayers[i] = False

