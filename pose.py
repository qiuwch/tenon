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
    pts = pd.read_csv('/q/cache/lsp_2d_3d/%04d.csv' % id)
    # Swap y an z axis

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
        ptx = pts.x[i] - pts.x[0]
        pty = pts.y[i] - pts.y[0]
        ptz = pts.z[i] - pts.z[0]
        controlEmpty.location.x = ptx + root.x
        controlEmpty.location.y = ptz + root.y# Swap y and z
        controlEmpty.location.z = - pty + root.z


def loadJointLocCSV(csvFile):
    import pandas as pd
    pts = pd.read_csv('/q/cache/lsp_2d_3d/%04d.csv' % id)
    
    pass


def createTestEditBone(id):
    # The mapping from csv to empty
    # Use this function with armature_visualize.blend
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

    import pandas as pd
    pts = pd.read_csv('/q/cache/lsp_2d_3d/%04d.csv' % id)

    # Load joint location from csv file.    
    loc = {}
    for i in range(len(pts.x)):
        jointName = order[i]
        loc[jointName] = mathutils.Vector((pts.x[i], pts.y[i], pts.z[i]))

    # Generate edit bones to show joint location

    editBones = [
        'back-bone', 'R-shldr', 'R-Uarm', 'R-Larm', 
        'L-shldr', 'L-Uarm', 'L-Larm', 'head',
        'R-hip', 'R-Uleg', 'R-Lleg', 'R-feet', 
        'L-hip', 'L-Uleg', 'L-Lleg', 'L-feet'
    ];

    import pandas as pd
    pts = pd.read_csv('/q/cache/lsp_2d_3d/%04d.csv' % id)

    # Mapping between bone and joint
    editBoneJointMapping = {
        'back-bone.head': 'root',
        'back-bone.tail': 'neck',
        'R-shldr.head': 'neck',
        'R-shldr.tail': 'shoulder.r',
        'R-Uarm.head': 'shoulder.r',
        'R-Uarm.tail': 'elbow.r',
        'R-Larm.head': 'elbow.r',
        'R-Larm.tail': 'wrist.r',
        'L-shldr.head': 'neck',
        'L-shldr.tail': 'shoulder.l',
        'L-Uarm.head': 'shoulder.l',
        'L-Uarm.tail': 'elbow.l',
        'L-Larm.head': 'elbow.l',
        'L-Larm.tail': 'wrist.l',
        'head.tail': 'headTop',
        'head.head': 'neck',
        'R-hip.head': 'root',
        'R-hip.tail': 'hip.r',
        'R-Uleg.head': 'hip.r',
        'R-Uleg.tail': 'knee.r',
        'R-Lleg.head': 'knee.r',
        'R-Lleg.tail': 'ankle.r',
        'R-feet.head': 'ankle.r',
        'R-feet.tail': 'foot.r',
        'L-hip.head': 'root',
        'L-hip.tail': 'hip.l',
        'L-Uleg.head': 'hip.l',
        'L-Uleg.tail': 'knee.l',
        'L-Lleg.head': 'knee.l',
        'L-Lleg.tail': 'ankle.l',
        'L-feet.head': 'ankle.l',
        'L-feet.tail': 'foot.l'
    };

    for editBoneName in editBones:
        # Create an edit bone to show joint location
        editBone = bpy.context.object.data.edit_bones.get(editBoneName)
        if not editBone:
            editBone = bpy.context.object.data.edit_bones.new(editBoneName)
        headJointName = editBoneJointMapping[editBoneName + '.head']
        tailJointName = editBoneJointMapping[editBoneName + '.tail']

        editBone.head = loc[headJointName]
        editBone.tail = loc[tailJointName]


