# Deprecated: Create mesh for skeleton generation
# TODO: rewrite this script.
import bpy
import bpy_extras
import tenon.config

selectedBones = {
    'shin.fk.L': [0, 0, 1],
    'shin.fk.R': [0, 1, 0],
    'thigh.fk.L': [0, 1, 1],
    'thigh.fk.R': [1, 0, 0],
    'head': [1, 0, 1],
    'foot.fk.L': [1, 1, 0],
    'foot.fk.R': [0, 0, 0],
    'hand.fk.L': [0, 0, 1],
    'hand.fk.R': [0, 1, 0],
    'forearm.fk.R': [0, 1, 1],
    'forearm.fk.L': [1, 0, 0],
    'upper_arm.fk.L': [1, 0, 1],
    'upper_arm.fk.R': [1, 1, 0],
    'neck': [0, 0, 0]
}

def world2camera(location):
    ''' Map the 3d coordinate to camera coordinate
    This is an excellent reference: http://blender.stackexchange.com/questions/882/how-to-find-image-coordinates-of-the-rendered-vertex 
    '''

    scene = bpy.context.scene
    cam = bpy.data.objects.get('Camera')
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, location)
    # co_2d is normalized device coordinate (NDC)

    # If you want pixel coords
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
            )
    return (round(co_2d.x * render_size[0]), round((1-co_2d.y) * render_size[1]))

def createMarker():
    ''' Create an UV sphere for each joint, then assign the material to the joints. '''
    obj = bpy.data.objects[tenon.config.human_model]

    for bone in obj.pose.bones:
        if not bone.name in selectedBones.keys(): # Ignore not related joints
            continue

        poseBone = bone
        boneName = bone.name
        armBone = obj.data.bones[boneName]

        location = poseBone.head
        layers = [False for i in range(20)]
        layers[3] = True # layer 4
        bpy.ops.mesh.primitive_uv_sphere_add(size=0.2, location=location, layers=layers) # set the layers of these balls
        objName = bone.name + 'Ball'
        ball = bpy.context.active_object
        ball.name = objName

        # Add material for rendering.
        mat = bpy.data.materials.new(name = bone.name + 'Material')
        mat.use_shadeless = True
        if len(ball.data.materials):
        	ball.data.materials[0] = mat
        else:
        	ball.data.materials.append(mat)
        mat.diffuse_color = selectedBones[bone.name]
