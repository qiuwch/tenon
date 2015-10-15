# Script to manipulate human pose
import os
import bpy
import mathutils
import math
import tenon.config

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
    # Make the retarget code here.
    bpy.ops.object.mode_set(mode='OBJECT')

    # Load data from exported csv file
    loc = readJointLocCSV(tenon.config.lspJointFile % id)
    if not loc:
        return

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
        # controlEmpty.location.x = pt.x + root.x
        # controlEmpty.location.y = pt.y + root.y
        # controlEmpty.location.z = pt.z + root.z
        controlEmpty.location.x = pt.x
        controlEmpty.location.y = pt.y
        controlEmpty.location.z = pt.z

    bpy.context.scene.update()  # This is super important

def getBoneLength():
    def getRestJointLoc(boneName, jointType):
        # Must get the location of edit bone here.
        print(boneName)
        obj = bpy.data.objects['human_model']
        editBone = obj.data.edit_bones[boneName] # TODO: FIX this
        if jointType == 'head':
            loc = editBone.head
        elif jointType == 'tail':
            loc = editBone.tail
        else:
            loc = None
        return loc

    def computeDistance(loc1, loc2):
        return (loc1 - loc2).length

    def getBoneLength(pair): 
        names = pair[0]

        [name1, sep, jointType1] = names[0].rpartition('.')
        loc1 = getRestJointLoc(name1, jointType1)

        [name2, sep, jointType2] = names[1].rpartition('.')
        loc2 = getRestJointLoc(name2, jointType2)

        length = computeDistance(loc1, loc2)

        return length

    # Modify this to see which strategy is better
    link = [
        [('root.head', 'neck.head'), (1, 2)],
        [('neck.head', 'head.tail'), (2, 9)], # The number is orderId in 3D skeleton

        [('neck.head', 'deltoid.R.tail'), (2, 6)],
        [('upper_arm.fk.R.head', 'upper_arm.fk.R.tail'), (6, 7)],
        [('forearm.fk.R.head', 'forearm.fk.R.tail'), (7, 8)],

        [('neck.head', 'deltoid.L.tail'), (2, 3)],
        [('upper_arm.fk.L.head', 'upper_arm.fk.L.tail'), (3, 4)],
        [('forearm.fk.L.head', 'forearm.fk.L.tail'), (4, 5)],

        [('neck.head', 'thigh.fk.R.head'), (2, 14)],        
        [('thigh.fk.R.head', 'thigh.fk.R.tail'), (14, 15)],
        [('shin.fk.R.head', 'shin.fk.R.tail'), (15, 16)],
        [('shin.fk.R.tail', 'toe.fk.R.tail'), (16, 17)],

        [('neck.head', 'thigh.fk.L.head'), (2, 10)],
        [('thigh.fk.L.head', 'thigh.fk.L.tail'), (10, 11)],
        [('shin.fk.L.head', 'shin.fk.L.tail'), (11, 12)],
        [('shin.fk.L.tail', 'toe.fk.L.tail'), (12, 13)]
    ]

    bpy.context.scene.objects.active = bpy.data.objects['human_model']
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in link:
        boneLength = getBoneLength(bone) # This is buggy
        print(boneLength)
    bpy.ops.object.mode_set(mode='OBJECT')

def retargetJointLocation(loc):
    def getJointLoc(boneName, jointType):
        # Must get the location of edit bone here.
        print(boneName)
        obj = bpy.data.objects['human_model']
        # bpy.context.scene.objects.active = bpy.data.objects['human_model']
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.context.scene.update()
        poseBone = obj.pose.bones[boneName]
        if jointType == 'head':
            loc = poseBone.head # Why the bone of poseBone is over shot a lot?
        elif jointType == 'tail':
            loc = poseBone.tail
        else:
            loc = None
        # editBone = obj.data.edit_bones[boneName] # TODO: FIX this
        # if jointType == 'head':
        #     loc = editBone.head
        # elif jointType == 'tail':
        #     loc = editBone.tail
        # else:
        #     loc = None
        # bpy.ops.object.mode_set(mode='OBJECT')
        print(loc)
        return loc

    def computeDistance(loc1, loc2):
        return (loc1 - loc2).length

    def getBoneLength(pair): 
        names = pair[0]

        [name1, sep, jointType1] = names[0].rpartition('.')
        loc1 = getJointLoc(name1, jointType1)

        [name2, sep, jointType2] = names[1].rpartition('.')
        loc2 = getJointLoc(name2, jointType2)

        length = computeDistance(loc1, loc2)

        return length

    print('Retarget the joint location to fit the human model')
    # Remapping the skeleton structure for this human.
    jointList = [
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

    # Modify this to see which strategy is better
    link = [
        [('root.head', 'neck.head'), (1, 2)],
        [('neck.head', 'head.tail'), (2, 9)], # The number is orderId in 3D skeleton

        [('neck.head', 'deltoid.R.tail'), (2, 6)],
        [('upper_arm.fk.R.head', 'upper_arm.fk.R.tail'), (6, 7)],
        [('forearm.fk.R.head', 'forearm.fk.R.tail'), (7, 8)],

        [('neck.head', 'deltoid.L.tail'), (2, 3)],
        [('upper_arm.fk.L.head', 'upper_arm.fk.L.tail'), (3, 4)],
        [('forearm.fk.L.head', 'forearm.fk.L.tail'), (4, 5)],

        [('neck.head', 'thigh.fk.R.head'), (2, 14)],        
        [('thigh.fk.R.head', 'thigh.fk.R.tail'), (14, 15)],
        [('shin.fk.R.head', 'shin.fk.R.tail'), (15, 16)],
        [('shin.fk.R.tail', 'toe.fk.R.tail'), (16, 17)],

        [('neck.head', 'thigh.fk.L.head'), (2, 10)],
        [('thigh.fk.L.head', 'thigh.fk.L.tail'), (10, 11)],
        [('shin.fk.L.head', 'shin.fk.L.tail'), (11, 12)],
        [('shin.fk.L.tail', 'toe.fk.L.tail'), (12, 13)]
    ]

    newLoc = {}
    newLoc['root'] = loc['root'] # Start from here
    # Do normalization for each bone

    # Switch to edit mode
    # bpy.context.scene.objects.active = bpy.data.objects['human_model']
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.context.scene.update()

    for bone in link:
        boneLength = getBoneLength(bone) # This is buggy

        joint1 = jointList[bone[1][0]-1] # TODO: change this ugly code later
        joint2 = jointList[bone[1][1]-1]
        src = loc[joint1]
        tgt = loc[joint2]

        vec = tgt - src
        # print('%.2f' % vec.length)
        vec.normalize()

        newSrc = newLoc[joint1]
        newTgt = newSrc + vec * boneLength
        print('%.2f %.2f' % (vec.length, boneLength))

        newLoc[joint2] = newTgt

    # Switch back to object mode
    # bpy.ops.object.mode_set(mode='OBJECT')

    return newLoc


def readJointLocCSV(csvFile, retarget=True):
    if not os.path.isfile(csvFile):
        print('Joint file %s does not exist.' % csvFile)
        return None

    print('Read joint information from csv file %s' % csvFile)
    # import pandas as pd
    # pts = pd.read_csv(csvFile)

    px = []; py = []; pz = []; jointNames = []
    with open(csvFile) as f:
        headline = f.readline()
        assert(headline.strip().lower() == 'name,x,y,z')

        line = f.readline()
        while line:
            [name,x,y,z] = line.strip().split(',')
            px.append(float(x))
            py.append(float(y))
            pz.append(float(z))
            jointNames.append(name)
            line = f.readline()

    # Load joint location from csv file.    
    loc = {}
    for i in range(len(px)):
        jointName = jointNames[i]

        # Swap y an z axis
        x = px[i] - px[0]
        y = pz[i] - pz[0]
        z = py[i] - py[0] # swap y and z
        z = -z
        loc[jointName] = mathutils.Vector((x, y, z))

    if retarget:
        loc = retargetJointLocation(loc)

    # Post-processing
    # Add tail
    addTail(loc)

    # Move the shoulder down
    vec = loc['neck'] - loc['root']
    offset = - vec * 0.3
    offJoints = ['shoulder.l', 'shoulder.r', 'elbow.l', 'elbow.r', 'wrist.l', 'wrist.r']
    for j in offJoints:
        loc[j] += offset

    return loc

def addTail(loc):
    # Use this to add a tail bone to structure
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


def animateEditBone(id, normalize=True):
    bpy.context.scene.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='EDIT')

    # The mapping from csv to empty
    # Use this function with armature_visualize.blend
    if normalize:
        loc = readJointLocCSV(tenon.config.lspJointFile % id)
    else:
        loc = readJointLocCSV(tenon.config.lspJointFile % id, retarget=False)

    if not loc:
        return


    # Generate edit bones to show joint location
    editBones = [ # I got these names from the poseprior dataset
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


