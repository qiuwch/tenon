# Script to manipulate human pose
import os
import bpy
import mathutils
import math
import tenon.config

# Generate edit bones to show joint location
bones = [ # I got these names from the poseprior dataset
    'back-bone', 'R-shldr', 'R-Uarm', 'R-Larm', 
    'L-shldr', 'L-Uarm', 'L-Larm', 'head',
    'R-hip', 'R-Uleg', 'R-Lleg', 'R-feet', 
    'L-hip', 'L-Uleg', 'L-Lleg', 'L-feet', 'tail'
];

# Mapping between bone and joint
posepriorJointMapping = {
    'back-bone': ['root','neck'],
    'R-shldr': ['neck','shoulder.r'],
    'R-Uarm': ['shoulder.r','elbow.r'],
    'R-Larm': ['elbow.r','wrist.r'],
    'L-shldr': ['neck','shoulder.l'],
    'L-Uarm': ['shoulder.l','elbow.l'],
    'L-Larm': ['elbow.l','wrist.l'],
    'head': ['neck','headTop'],
    'R-hip': ['root','hip.r'],
    'R-Uleg': ['hip.r','knee.r'],
    'R-Lleg': ['knee.r','ankle.r'],
    'R-feet': ['ankle.r','foot.r'],
    'L-hip': ['root','hip.l'],
    'L-Uleg': ['hip.l','knee.l'],
    'L-Lleg': ['knee.l','ankle.l'],
    'L-feet': ['ankle.l','foot.l'],
    'tail': ['root', 'tail']
}

# Mapping between bone and joint
makehumanJointMapping = {
    'back-bone': ['root.head', 'neck.head'],
    'R-shldr': ['neck.head', 'deltoid.R.tail'],
    'R-Uarm': ['upper_arm.fk.R.head', 'upper_arm.fk.R.tail'],
    'R-Larm': ['forearm.fk.R.head', 'forearm.fk.R.tail'],
    'L-shldr': ['neck.head', 'deltoid.L.tail'],
    'L-Uarm': ['upper_arm.fk.L.head', 'upper_arm.fk.L.tail'],
    'L-Larm': ['forearm.fk.R.head', 'forearm.fk.R.tail'],
    'head': ['head.tail', 'neck.head'],
    'R-hip': ['root.head', 'thigh.fk.R.head'],
    'R-Uleg': ['thigh.fk.R.head', 'thigh.fk.R.tail'],
    'R-Lleg': ['shin.fk.R.head', 'shin.fk.R.tail'],
    'R-feet': ['shin.fk.R.tail', 'toe.fk.R.tail'],
    'L-hip': ['root.head', 'thigh.fk.L.head'],
    'L-Uleg': ['thigh.fk.L.head', 'thigh.fk.L.tail'],
    'L-Lleg': ['shin.fk.L.head', 'shin.fk.L.tail'],
    'L-feet': ['shin.fk.L.tail', 'toe.fk.L.tail'],
    'tail': ['root.head', 'root.tail'],
}



def animateEditBone(id, normalize=True):
    # The mapping from csv to empty
    # Use this function with armature_visualize.blend
    if normalize:
        loc = readJointLocCSV(tenon.config.lspJointFile % id)
    else:
        loc = readJointLocCSV(tenon.config.lspJointFile % id, retarget=False)

    if not loc:
        return

    bpy.context.scene.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='EDIT')
    for editBoneName in bones:
        # Create an edit bone to show joint location
        editBone = bpy.context.object.data.edit_bones.get(editBoneName)
        if not editBone:
            editBone = bpy.context.object.data.edit_bones.new(editBoneName)
        headJointName = posepriorJointMapping[editBoneName][0]
        tailJointName = posepriorJointMapping[editBoneName][1]

        editBone.head = loc[headJointName]
        editBone.tail = loc[tailJointName]


def animateCP(id):
    # Make the retarget code here.
    # Load data from exported csv file
    loc = readJointLocCSV(tenon.config.lspJointFile % id)
    if not loc:
        return

    obj = bpy.data.objects['human_model']
    root = obj.pose.bones['root'].head

    bpy.ops.object.mode_set(mode='OBJECT')
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
        controlEmpty.location.x = pt.x
        controlEmpty.location.y = pt.y
        controlEmpty.location.z = pt.z

    bpy.context.scene.update()  # This is super important

def getReferenceArmature():
    # Get the bone length defined by the armature I want to target to
    def getRestJointLoc(boneName, jointType):
        # Must get the location of edit bone here.
        obj = bpy.data.objects['human_model']
        editBone = obj.data.edit_bones[boneName]
        if jointType == 'head':
            loc = editBone.head
        elif jointType == 'tail':
            loc = editBone.tail
        else:
            loc = None
        return loc

    def computeDistance(loc1, loc2):
        return (loc1 - loc2).length

    def getBoneLength(boneName): 
        boneHead = makehumanJointMapping[boneName][0]
        boneTail = makehumanJointMapping[boneName][1]

        [name1, sep, jointType1] = boneHead.rpartition('.')
        loc1 = getRestJointLoc(name1, jointType1)

        [name2, sep, jointType2] = boneTail.rpartition('.')
        loc2 = getRestJointLoc(name2, jointType2)

        length = computeDistance(loc1, loc2)

        return length

    bpy.context.scene.objects.active = bpy.data.objects['human_model']
    bpy.ops.object.mode_set(mode='EDIT')

    refArmature = {}
    for bone in bones:
        boneLength = getBoneLength(bone) # This is buggy
        refArmature[bone] = boneLength

    bpy.ops.object.mode_set(mode='OBJECT')

    return refArmature

def retargetJointLocation(loc):
    print('Retarget the joint location to fit the human model')
    newLoc = {}
    newLoc['root'] = loc['root'] # Start from here
    # Do normalization for each bone

    refArmature = getReferenceArmature()
    for bone in bones:
        boneLength = refArmature[bone]

        joint1 = posepriorJointMapping[bone][0] # TODO: change this ugly code later
        joint2 = posepriorJointMapping[bone][1]
        src = loc[joint1]
        tgt = loc[joint2]

        vec = tgt - src
        # print('%.2f' % vec.length)
        vec.normalize()

        newSrc = newLoc[joint1]
        newTgt = newSrc + vec * boneLength

        newLoc[joint2] = newTgt

    return newLoc


def readJointLocCSV(csvFile, retarget=True):
    if not os.path.isfile(csvFile):
        print('Joint file %s does not exist.' % csvFile)
        return None

    print('Read joint information from csv file %s' % csvFile)

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

    # Add tail
    addTail(loc)        

    if retarget:
        loc = retargetJointLocation(loc)

    # Post-processing

    # Move the shoulder down
    vec = loc['neck'] - loc['root']
    offset = - vec * 0.32
    offJoints = ['shoulder.l', 'shoulder.r', 'elbow.l', 'elbow.r', 'wrist.l', 'wrist.r']
    for j in offJoints:
        loc[j] += offset

    return loc

def addTail(loc):
    # Use this to add a tail bone to structure
    # Create a tail for rotation control
    vec1 = loc['shoulder.l'] - loc['shoulder.r']
    vec2 = loc['neck'] - loc['root']

    vec = cross(vec1, vec2)
    orintationVec = [
        loc['hip.r'] - loc['root'],
        loc['hip.l'] - loc['root'],
        # loc['knee.l'] - loc['hip.l'],
        # loc['knee.r'] - loc['hip.r']
        loc['foot.l'] - loc['ankle.l'],
        loc['foot.r'] - loc['ankle.r']
    ]

    sameDirection = [dot(v, vec)/(v.length * vec.length) for v in orintationVec]

    if sum(sameDirection) > 0:
        vec = -vec

    vec = normalize(vec)
    loc['tail'] = loc['root'] + 5 * vec

def dot(vec1, vec2):
    return vec1.dot(vec2)

def cross(vec1, vec2):
    return vec1.cross(vec2)

def normalize(vec):
    vec.normalize()
    return vec


