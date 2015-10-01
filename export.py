# Utility script to export 3d joint location to txt file
import bpy
import math
from tenon.config import selectedBones, connections

version = 'v4'

def testJointRot():
    ''' Test the joint rotation transform code in MATLAB '''
    import tenon.pose
    from tenon.config import TMP_DIR
    tenon.pose.rest()
    bpy.context.scene.update() # TODO: important to update the scene before retriving information!
    export3dJoints(TMP_DIR + 'rest.csv')
    tenon.pose.testPose()
    bpy.context.scene.update()
    export3dJoints(TMP_DIR + 'animate.csv')

    # Also save the connection matrix?
    aIndices = []
    bIndices = []
    for edge in connections:
        a = edge[0]
        b = edge[1]

        def findIndex(boneName):
            for i in range(len(selectedBones)):
                if selectedBones[i][0] + '.' + selectedBones[i][1] == boneName:
                    return i
            print('%s not found' % boneName)

        aIndex = findIndex(a)
        bIndex = findIndex(b)

        aIndices.append(aIndex)
        bIndices.append(bIndex)

    f = open(TMP_DIR + 'connection.csv', 'w')
    f.write(','.join([str(v) for v in aIndices]) + '\n')
    f.write(','.join([str(v) for v in bIndices]) + '\n')
    f.close()

def export3dJoints(filename):
    def _vec2StrArray(vec):
        # convert blender vector to python string array
        return [str(vec.x), str(vec.y), str(vec.z)]

    def _arr2StrArray(arr):
        return ['%.5f' % v for v in arr]

    def _mat2RowArray(mat):
        arr = []
        for row in range(4):
            for col in range(4):
                arr.append(mat[row][col])
        return arr

    print(version)
    """ Export the joint 3d locations to a text file """
    obj = bpy.data.objects['human_model']

    f = open(filename, 'w')

    lines = []
    for v in selectedBones:
        name = v[0]
        poseBone = obj.pose.bones.get(name)

        assert(poseBone != None)

        jointType = v[1]
        if jointType == 'head':
            location = poseBone.head
        elif jointType == 'tail':
            location = poseBone.tail

        # line = ','.join([poseBone.name, str(location.x), str(location.y), str(location.z)]) + '\n'
        pos = [location.x, location.y, location.z]
        rot = [poseBone.rotation_euler.x, poseBone.rotation_euler.y, poseBone.rotation_euler.z]
        matrixBasis = _mat2RowArray(poseBone.matrix_basis)
        matrixLocal = _mat2RowArray(poseBone.bone.matrix_local)
        matrix = _mat2RowArray(poseBone.matrix)

        ## Also export parent name
        cols = [poseBone.name, poseBone.parent.name] + _arr2StrArray(pos + rot + matrixBasis + matrixLocal + matrix)
        line = ','.join(cols) + '\n'

        lines.append(line)

    lines.insert(0, ','.join(['header' + str(v) for v in range(len(cols))]) + '\n')

    for line in lines:
        f.write(line)
    f.close()

def restPose():
    ''' Save the rest pose of the armature '''
    pass

def boneLength():
    def getJointLoc(boneName, jointType):
        obj = bpy.data.objects['human_model']
        poseBone = obj.pose.bones[boneName]
        if jointType == 'head':
            loc = poseBone.head
        elif jointType == 'tail':
            loc = poseBone.tail
        else:
            loc = None
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

    ''' Save the bone length '''
    # Define the two end point of a bone, also define the tree structure
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

    with open('/Users/qiuwch/Downloads/boneLength.csv', 'w') as f:
        for pair in link:
            length = getBoneLength(pair)
            line = '%s,%s,%d,%d,%.6f' % (pair[0][0], pair[0][1], pair[1][0], pair[1][1], length)
            print(line)
            f.write(line + '\n')


'''
arm = selectedPoseBone()
A = arm.parent.bone.matrix_local
A.invert()
arm.parent.matrix * A * arm.bone.matrix_local * arm.matrix_basis
'''