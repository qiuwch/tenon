# Demo script to show how to generate random lighting
tenonpath = '/q/workspace/tenon'
import sys; sys.path.append(tenonpath) # Install tenon
import tenon
import os

def world2camera(location):
    import bpy, bpy_extras
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


def exportJoint():
    '''
    Export the joint location as 2d coordinates
    '''
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

    obj = tenon.obj.get('m_c_1')
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

def serializeJointInfo(filename, joints):
    with open(filename, 'w') as f:
        for j in joints:
            f.write('%s,%s\n' % (j[0], ','.join([str(v) for v in j[1]])))

def main():
    '''
    Manually set up:
    - Let camera track the head of human model
    '''
    # tenon.render.DepthMode.disable()
    # tenon.render.writevideo('video/')
    # tenon.logging.info('Complete rendering video')

    # tenon.render.DepthMode.enable()
    # tenon.render.writevideo('depth/')
    # tenon.logging.info('Complete rendering depth')

    # Output the joint location
    for fid in range(10):
        tenon.obj.scene.frame_set(fid)
        # set to frame
        joints = exportJoint()
        serializeJointInfo('joint/%04d.csv' % fid, joints)


tenon.run(__file__, './demo_mocap1.blend')
# tenon.run(__file__, '../../demo.blend')
if tenon.inblender():
    main()
