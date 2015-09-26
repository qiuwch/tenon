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

'''
arm = selectedPoseBone()
A = arm.parent.bone.matrix_local
A.invert()
arm.parent.matrix * A * arm.bone.matrix_local * arm.matrix_basis
'''