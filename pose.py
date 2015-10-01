# Script to manipulate human pose
import bpy
import mathutils
import math
def rest():
    """ Set the human body to rest pose """

    # scn.objects.active = rig
    # TODO: Bug fix!! This code can not work with locked property
    # bpy.ops.object.mode_set(mode='POSE')
    # bpy.ops.pose.select_all(action='SELECT')
    # bpy.ops.pose.rot_clear()
    # bpy.ops.pose.loc_clear()
    # bpy.ops.pose.scale_clear()

    obj = bpy.data.objects['human_model']
    for bone in obj.pose.bones:
        bone.matrix_basis = mathutils.Matrix() # Set it to identity matrix

def TPose():
    ''' This is not working at this moment '''
    version = 'v3'
    print(version)

    obj = bpy.data.objects['human_model']
    for poseBone in obj.pose.bones:
        poseBone.matrix_basis = mathutils.Matrix() # Set it to identity matrix
        # poseBone.bone.matrix_local = mathutils.Matrix() # this is very wrong

        old = poseBone.bone.matrix_local

        loc, rot, sca = old.decompose()

        transMat = mathutils.Matrix.Translation(loc)
        scaleMat = mathutils.Matrix.Scale(sca[0], 4, (1, 0, 0)) * mathutils.Matrix.Scale(sca[1], 4, (0, 1, 0)) * mathutils.Matrix.Scale(sca[2], 4, (0, 0, 1))

        # rotMat = mathutils.Matrix.Rotation(rot)

        # poseBone.bone.matrix_local = transMat # * rotMat * scaleMat
        # Without scale is weird
        poseBone.bone.matrix_local = transMat * scaleMat


def testPose():
    ''' Only change the forearem '''
    human = bpy.data.objects['human_model']

    forearm = human.pose.bones['forearm.fk.L']
    upper_arm = human.pose.bones['upper_arm.fk.L']

    def setBoneYZXEuler(bone, x, y, z):
        print(bone.rotation_mode)
        assert(bone.rotation_mode == 'YZX')

        # Just some random number for test
        bone.rotation_euler.x = x / 180 * math.pi # This is radius
        bone.rotation_euler.y = y / 180 * math.pi
        bone.rotation_euler.z = z / 180 * math.pi

    setBoneYZXEuler(forearm, 90, 0, 0)
    setBoneYZXEuler(upper_arm, 43, 54, 65)

def createControlPoint():
    names = [ # Order does not matter
        'ankle.r',
        'knee.r',
        'hip.r',
        'hip.l',
        'knee.l',
        'ankle.l',
        'wrist.r',
        'elbow.r',
        'shoulder.r',
        'shoulder.l',
        'elbow.l',
        'wrist.l',
        'neck',
        'headTop',
        'root'
    ]
    for jointName in names:
        controlEmpty = bpy.data.objects.get(jointName)
        if controlEmpty == None:
            bpy.ops.object.empty_add()
            controlEmpty = bpy.context.object
            controlEmpty.name = jointName

    # setup joint constraint manually

def animateCP(id):
    # Load data from exported csv file
    import pandas as pd
    pts = pd.read_csv('/q/cache/lsp_2d_3d/%04d.csv' % (id+1))

    # The mapping from csv to empty
    order = [
        'root',
        'neck',
        'shoulder.l',
        'elbow.l',
        'wrist.l',
        'shoulder.r',
        'elbow.r',
        'wrist.r',
        'headTop',
        'hip.l',
        'knee.l',
        'ankle.l',
        'foot.l',
        'hip.r',
        'knee.r',
        'ankle.r',
        'foot.r'
    ]
    obj = bpy.data.objects['human_model']
    root = obj.pose.bones['root'].head
    #
    for i in range(len(pts.x)):
        jointName = order[i]
        controlEmpty = bpy.data.objects.get(jointName)
        if controlEmpty == None:
            # bpy.ops.object.empty_add()
            # controlEmpty = bpy.context.object
            # controlEmpty.name = jointName
            continue
        # 
        controlEmpty.location.x = pts.x[i] - pts.x[0] + root.x
        controlEmpty.location.y = pts.y[i] - pts.y[0] + root.y
        controlEmpty.location.z = pts.z[i] - pts.z[0] + root.z
