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

def animateCP(id):
    bpy.ops.object.mode_set(mode='OBJECT')

    # Load data from exported csv file
    loc = readJointLocCSV('/q/cache/lsp_2d_3d/%04d.csv' % id)

    obj = bpy.data.objects['human_model']
    root = obj.pose.bones['root'].head

    jointNames = loc.keys()
    # for i in range(len(jointNames)):
    for jointName in jointNames:
        # jointName = jointNames[i]
        controlEmpty = bpy.data.objects.get(jointName)
        if controlEmpty == None:
            bpy.ops.object.empty_add()
            controlEmpty = bpy.context.object
            controlEmpty.name = jointName

        pt = loc[jointName]
        controlEmpty.location.x = pt.x + root.x
        controlEmpty.location.y = pt.y + root.y
        controlEmpty.location.z = pt.z + root.z


def readJointLocCSV(csvFile):
    print('Read joint information from csv file %s' % csvFile)
    # import pandas as pd
    # pts = pd.read_csv(csvFile)

    px = []; py = []; pz = []
    with open(csvFile) as f:
        headline = f.readline()
        assert(headline.strip().lower() == 'x,y,z')

        line = f.readline()
        while line:
            [x,y,z] = line.strip().split(',')
            px.append(float(x))
            py.append(float(y))
            pz.append(float(z))
            line = f.readline()

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

    # Load joint location from csv file.    
    loc = {}
    for i in range(len(px)):
        jointName = order[i]

        # Swap y an z axis
        x = px[i] - px[0]
        y = pz[i] - pz[0]
        z = py[i] - py[0] # swap y and z
        z = -z
        loc[jointName] = mathutils.Vector((x, y, z))

    # Create a tail for rotation control
    vec1 = loc['hip.l'] - loc['root']
    vec2 = loc['hip.r'] - loc['root']
    back = loc['neck'] - loc['root']

    vec = cross(vec1, vec2)
    if (dot(vec, back) > 0):
        print(dot(vec, back))
        vec = -vec

    cosTheta = dot(vec, back) / (vec.length * back.length)
    # print(cosTheta)
    vec = vec - vec.length * cosTheta * back / back.length  # Make the vec perpendicular to back
    # print(vec.length)

    vec = normalize(vec)
    loc['tail'] = loc['root'] + 5 * vec

    return loc

def dot(vec1, vec2):
    return vec1.dot(vec2)
    # return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z

def cross(vec1, vec2):
    return vec1.cross(vec2)
    # x = vec1.y * vec2.z - vec1.z * vec2.y
    # y = vec1.x * vec2.z - vec1.z * vec2.x
    # z = vec1.x * vec2.y - vec1.y * vec2.x
    # vec = mathutils.Vector(x, y, z)
    # return vec 

def normalize(vec):
    vec.normalize()
    return vec
    # length = math.sqrt(vec.x ** 2 + vec.y ** 2 + vec.z ** 2)
    # newVec = mathutils.Vector(vec.x / length, vec.y / length, vec.z / length)
    # return newVec


def animateEditBone(id):
    bpy.context.scene.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='EDIT')

    # The mapping from csv to empty
    # Use this function with armature_visualize.blend
    loc = readJointLocCSV('/q/cache/lsp_2d_3d/%04d.csv' % id)
    # Generate edit bones to show joint location

    editBones = [
        'back-bone', 'R-shldr', 'R-Uarm', 'R-Larm', 
        'L-shldr', 'L-Uarm', 'L-Larm', 'head',
        'R-hip', 'R-Uleg', 'R-Lleg', 'R-feet', 
        'L-hip', 'L-Uleg', 'L-Lleg', 'L-feet', 'tail'
    ];

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
        'L-feet.tail': 'foot.l',
        'tail.head': 'root',
        'tail.tail': 'tail'
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


