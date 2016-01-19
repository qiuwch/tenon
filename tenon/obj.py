import bpy
import tenon.logging
import mathutils

scene = bpy.data.scenes['Scene']
'''
The setup of scene should be done in the blender editor which is more efficient than with code
'''
# Control render config
renderLayer = scene.render.layers['RenderLayer']
sceneLayers = scene.layers
renderLayers = scene.render.layers['RenderLayer'].layers

def get(name):
    '''
    Property of object including location, etc, more detail see the documentation of blender
    http://www.blender.org/api/blender_python_api_2_76_2/bpy.types.Object.html#bpy.types.Object
    '''
    obj = bpy.data.objects.get(name)
    if not obj:
        tenon.logging.warning('Object "%s" does not exist' % name)

    return obj

class Lamp:
    class LampType:
        Point, Sun, Spot, Hemi, Area = range(5)

    def create(name, type=LampType.Point):
        '''
        Create a lamp and return it, right now only support point light
        '''
        tenon.logging.debug('Create a lamp called %s' % name)
        obj = bpy.data.objects.get(name)
        # It seems tricky to modify the lamp name, which needs to modify lamp and obj name together

        if not obj:
            # from: http://www.blender.org/api/blender_python_api_2_66_6/bpy.types.Object.html
            # Create new lamp datablock
            scene = bpy.context.scene
            lamp_data = bpy.data.lamps.new(name=name, type='POINT')
            obj = bpy.data.objects.new(name=name, object_data=lamp_data)
            scene.objects.link(obj)

            # An alternative way
            # ret = bpy.ops.object.lamp_add(type='POINT'), Does not support name
            # checkOp(ret)

        lamp = bpy.data.lamps.get(name)
        return lamp

    def get(name):
        lamp = bpy.data.lamps.get(name)
        return lamp