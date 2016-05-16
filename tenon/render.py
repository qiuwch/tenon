import bpy
import tenon
import tenon.logging as L
import tenon.util as U
import os

def write(filename):
    filename = bpy.path.abspath(os.path.expanduser(filename))
    tenon.obj.scene.render.filepath = filename
    tenon.obj.scene.update()
    bpy.ops.render.render(write_still=True)
    L.debug('Write file to %s', L.prettify_filename(filename))

def writevideo(filename, format=''):
    '''
    Render a video with blender
    http://blender.stackexchange.com/questions/6082/rendering-into-video-with-blender-in-python-frames-to-video
    '''
    # for scene in bpy.data.scenes:
    # scene = tenon.obj.get('Scene')
    scene = bpy.data.scenes[0]
    scene.render.filepath = filename
    data_context = {"blend_data": bpy.context.blend_data, "scene": scene}
    bpy.ops.render.render(data_context, animation=True)

class DepthMode:
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
            tenon.logging.error('Error in setuping up depth mode, renderLayersNode and compositeNode are missing')

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


class PaintMode:
    '''
    Render vertex paint, useful for adding annotation
    '''
    @classmethod
    def enable(cls, obj):
        # cls.renderLayer.use_sky = False
        '''
        Enable paint mode for a specific object
        This won't take effect if no material is assigned
        '''
        if obj:
            if len(obj.material_slots.items()) == 0:
                tenon.logging.warning('No material is defined for object: %s' % obj.name)
            for slot in obj.material_slots:
                cls._materialOn(slot.material)
        else:
            tenon.logging.warning('Enable paint mode: Object not exist')

    @classmethod
    def disable(cls, obj):
        # cls.renderLayer.use_sky = cls.use_sky
        '''
        Disable Paint Mode, reverse previous operation
        '''
        if obj:
            for slot in obj.material_slots:
                cls._materialOff(slot.material)
        else:
            tenon.logging.warning('Disable paint mode: Object not exist')

    @classmethod
    def _materialOn(cls, material):
        if material:
            material.use_shadeless = True
            material.use_vertex_color_paint = True

            material.use_transparency = False
            for i in range(len(material.use_textures)):
                material.use_textures[i] = False
        else:
            L.warning('Material on: input material is None')

    @classmethod
    def _materialOff(cls, material):
        if material:
            material.use_shadeless = False
            material.use_vertex_color_paint = False

            material.use_transparency = True
            for i in range(len(material.use_textures)):
                material.use_textures[i] = True




