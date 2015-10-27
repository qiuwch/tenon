# Script to manipulate human pose
import os
import bpy
import mathutils
import tenon.config
import logging
from tenon.core import Models

def animateEditBone(id, normalize=True):
    # The mapping from csv to empty
    # Use this function with armature_visualize.blend
    if normalize:
        loc = Retarget.readJointLocCSV(tenon.config.lspJointFile % id)
    else:
        loc = Retarget.readJointLocCSV(tenon.config.lspJointFile % id, retarget=False)

    if not loc:
        return

    bpy.context.scene.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='EDIT')
    for editBoneName in Retarget.bones:
        # Create an edit bone to show joint location
        editBone = bpy.context.object.data.edit_bones.get(editBoneName)
        if not editBone:
            editBone = bpy.context.object.data.edit_bones.new(editBoneName)
        headJointName = Retarget.posepriorJointMapping[editBoneName][0]
        tailJointName = Retarget.posepriorJointMapping[editBoneName][1]

        editBone.head = loc[headJointName]
        editBone.tail = loc[tailJointName]


def animateCP(id):
    # Make the retarget code here.
    # Load data from exported csv file
    loc = Retarget.readJointLocCSV(tenon.config.lspJointFile % id)
    if not loc:
        return

    # obj = Models.humanModel()
    # root = obj.pose.bones['root'].head

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
        logging.debug('Move %s to %s' % (jointName, str(pt)))

        controlEmpty.location.x = pt.x
        controlEmpty.location.y = pt.y
        controlEmpty.location.z = pt.z

    bpy.context.scene.update()  # This is super important




class Retarget:
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


    @classmethod
    def addTail(cls, loc):
        # Use this to add a tail bone to structure
        # Create a tail for rotation control
        # vec1 = loc['shoulder.l'] - loc['shoulder.r']
        logging.info('Add a tail bone to the armature')
        vec1 = loc['shoulder.r'] - loc['shoulder.l']
        vec2 = loc['neck'] - loc['root']

        vec = vec1.cross(vec2)

        # It is not necessary to check the tail orientation, since we know the left and right of the joints

        # orintationVec = [
        #     loc['hip.r'] - loc['root'],
        #     loc['hip.l'] - loc['root'],
        #     # loc['knee.l'] - loc['hip.l'],
        #     # loc['knee.r'] - loc['hip.r']
        #     loc['foot.l'] - loc['ankle.l'],
        #     loc['foot.r'] - loc['ankle.r']
        # ]

        # sameDirection = [dot(v, vec)/(v.length * vec.length) for v in orintationVec]

        # if sum(sameDirection) > 0:
        #     vec = -vec

        vec.normalize()
        loc['tail'] = loc['root'] + 5 * vec

    @classmethod
    def readJointLocCSV(cls, csvFile, retarget=True):
        if not os.path.isfile(csvFile):
            logging.error('Joint file %s does not exist.' % csvFile)
            return None

        logging.info('Read joint information from csv file %s' % csvFile)

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
        Retarget.addTail(loc)        

        # Move the shoulder down
        # Do this before length normalization, because this operation can affect bone length
        vec = loc['neck'] - loc['root']
        offset = vec * 0.32
        # offset = -vec * 0
        # offJoints = ['shoulder.l', 'shoulder.r', 'elbow.l', 'elbow.r', 'wrist.l', 'wrist.r']
        offJoints = ['neck', 'headTop']
        for j in offJoints:
            loc[j] += offset

        # Make the bone length fit the human model
        if retarget:
            loc = Retarget.retargetJointLocation(loc)

        return loc

    @classmethod
    def retargetJointLocation(cls, loc):
        logging.info('Retarget the joint location to fit the human model')
        newLoc = {}
        newLoc['root'] = loc['root'] # Start from here
        # Do normalization for each bone

        refArmature = Retarget.getReferenceArmature()
        for bone in Retarget.bones:
            boneLength = refArmature[bone]

            joint1 = Retarget.posepriorJointMapping[bone][0] # TODO: change this ugly code later
            joint2 = Retarget.posepriorJointMapping[bone][1]
            src = loc[joint1]
            tgt = loc[joint2]

            vec = tgt - src
            # print('%.2f' % vec.length)
            vec.normalize()

            newSrc = newLoc[joint1]
            newTgt = newSrc + vec * boneLength

            newLoc[joint2] = newTgt

        return newLoc

    @classmethod
    def getReferenceArmature(cls):
        # Get the bone length defined by the armature I want to target to
        def getRestJointLoc(boneName, jointType):
            # Must get the location of edit bone here.
            obj = Models.humanModel()
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
            boneHead = Retarget.makehumanJointMapping[boneName][0]
            boneTail = Retarget.makehumanJointMapping[boneName][1]

            [name1, sep, jointType1] = boneHead.rpartition('.')
            loc1 = getRestJointLoc(name1, jointType1)

            [name2, sep, jointType2] = boneTail.rpartition('.')
            loc2 = getRestJointLoc(name2, jointType2)

            length = computeDistance(loc1, loc2)

            return length

        bpy.context.scene.objects.active = Models.humanModel()
        bpy.ops.object.mode_set(mode='EDIT')

        refArmature = {}
        for bone in Retarget.bones:
            boneLength = getBoneLength(bone) # This is buggy
            refArmature[bone] = boneLength

        bpy.ops.object.mode_set(mode='OBJECT')

        return refArmature


class Constraint:
    controlPointNames = ['root', 'neck', 'shoulder.l', 'elbow.l', 'wrist.l', 'shoulder.r'
        , 'elbow.r', 'wrist.r', 'headTop', 'hip.l', 'knee.l', 'ankle.l', 'foot.l'
        , 'hip.r', 'knee.r', 'ankle.r', 'foot.r']

    @classmethod
    def createControlPoint(cls):
        bpy.ops.object.mode_set(mode='OBJECT')
        for p in cls.controlPointNames:
            controlEmpty = bpy.data.objects.get(p)
            if not controlEmpty:
                bpy.ops.object.empty_add()
                controlEmpty = bpy.context.object
                controlEmpty.name = p  

    def __init__(self):
        self.boneName = ''
        self.type = ''
        self.target = ''
        self.parameters = {}

    def apply(self):
        self.constraintName = '%s_%s' % (self.type, self.target)
        model = Models.humanModel()
        logging.info('Setting up constraint %s, %s' % (self.boneName, self.target))

        bone = model.pose.bones.get(self.boneName)
        if not bone:
            logging.error('The bone %s can not be found' % self.boneName)

        c = bone.constraints.get(self.constraintName)
        if c:
            logging.info('Constraint already exist')
        else:
            c = bone.constraints.new(self.type)

        targetObject = bpy.data.objects.get(self.target)
        if not targetObject:
            logging.error('The target object %s can not be found' % self.target)
        c.target = targetObject

        for k in self.parameters:
            logging.debug('Setup parameter %s:%s' % (k, self.parameters[k]))
            if k not in dir(c):
                logging.error('Parameter %s is not valid' % k)
            else:
                setattr(c, k, self.parameters[k])

    @classmethod
    def setup(cls):
        constraints = [
            # Set up constraints
            ['root', 'root', 'COPY_LOCATION'],
            ['root', 'tail', 'TRACK_TO', {'track_axis': 'TRACK_Y'}],
            # ['root', 'headTop', 'Track To', {'track_axis': 'z'}]
            ['root', 'headTop', 'LOCKED_TRACK', {'track_axis': 'TRACK_Z', 'lock_axis': 'LOCK_Y'}],
            ['chest-1', 'neck', 'IK'],
            ['deltoid.L', 'shoulder.l', 'IK', {'chain_count': 2}],
            ['upper_arm.fk.L', 'elbow.l', 'IK', {'chain_count': 1}],
            ['forearm.fk.L', 'wrist.l', 'IK', {'chain_count': 1}],
            ['deltoid.R', 'shoulder.r', 'IK', {'chain_count': 2}],
            ['upper_arm.fk.R', 'elbow.r', 'IK', {'chain_count': 1}],
            ['forearm.fk.R', 'wrist.r', 'IK', {'chain_count': 1}],
            ['thigh.fk.L', 'knee.l', 'IK', {'chain_count': 1}],
            ['shin.fk.L', 'ankle.l', 'IK', {'chain_count': 1}],
            ['thigh.fk.R', 'knee.r', 'IK', {'chain_count': 1}],
            ['shin.fk.R', 'ankle.r', 'IK', {'chain_count': 1}]
        ]

        cls.createControlPoint()

        for v in constraints:
            c = Constraint()
            c.boneName = v[0]
            c.target = v[1]
            c.type = v[2]
            if len(v) == 4: # parameters is optional
                c.parameters = v[3]
            c.apply()


    



