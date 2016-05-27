'''
Define a set of functions to read lsp 2D ground truth annotation
Demo code for interactive shell
import sys; sys.path.append('/q/workspace/tenon/examples/');
sys.path.append('/q/workspace/tenon/')
import lsppose
'''
import tenon
import tenon.logging as L
import os, glob



if tenon.inblender():
    '''
    Functions and classes only available for blender
    '''
    # The real work should only happen in blender
    import bpy, mathutils
    import tenon.util as U

    class Models:
        '''
        Provide access to mesh data in the scene
        '''
        def __init__(self):
            '''
            Find human model in the scene
            '''
            keys = bpy.data.armatures.keys()
            L.debug('Get %d armatures %s' % (len(keys), keys))

            modelNames = []
            for k in keys:
                humanModel = bpy.data.objects.get(k)
                humanBody = bpy.data.objects.get('%s:Body' % k)
                if humanModel and humanBody:
                    L.debug('Model %s exists' % k)
                    modelNames.append(k)
                else:
                    L.debug('Model %s not exist' % k)

            if len(modelNames) != 1:
                L.error('%d is invalid number of human models' % len(modelNames))
                return

            self.modelName = modelNames[0]

        def humanModel(self):
            '''
            Return human model
            '''
            return tenon.obj.get(self.modelName)

        def _getSemanticPart(self, types):
            for t in types:
                obj = tenon.obj.get('%s:%s' % (self.modelName, t))
                if obj:
                    return obj

            tenon.warning('None of %s exists' % types)


        def bodyMesh(self):
            types = ['Body']
            return self._getSemanticPart(types)

        def upperCloth(self): # TODO: consider rewrite this, not robust
            types = ['tshirt02']
            return self._getSemanticPart(types)

        def lowerCloth(self):
            types = ['jeans01']
            return self._getSemanticPart(types)

        def hair(self):
            types = ['mhair01', 'mhair02']
            return self._getSemanticPart(types)

        def eye(self):
            types = ['HighPolyEyes']
            return self._getSemanticPart(types)

    models = Models()

    class Retarget:
        '''
        Fit joint location data to armature
        '''
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
            L.info('Add the tail position to the armature')
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
            '''
            Return a dictionary containing location for each joint
            '''
            csvFile = os.path.expanduser(csvFile)
            if not os.path.isfile(csvFile):
                L.error('Joint file %s does not exist.' % csvFile)
                return None

            L.info('Read joint information from csv file %s' % csvFile)

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
            L.info('Retarget the joint location to fit the human model')
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
                obj = models.humanModel()
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

            bpy.context.scene.objects.active = models.humanModel()
            bpy.ops.object.mode_set(mode='EDIT')

            refArmature = {}
            for bone in Retarget.bones:
                boneLength = getBoneLength(bone) # This is buggy
                refArmature[bone] = boneLength

            bpy.ops.object.mode_set(mode='OBJECT')

            return refArmature

    class Constraint:
        '''
        Utilities to setup constraints in the scene.
        '''
        controlPointNames = ['root', 'neck', 'shoulder.l', 'elbow.l', 'wrist.l', 'shoulder.r'
            , 'elbow.r', 'wrist.r', 'headTop', 'hip.l', 'knee.l', 'ankle.l', 'foot.l'
            , 'hip.r', 'knee.r', 'ankle.r', 'foot.r', 'tail']

        @classmethod
        def createControlPoint(cls):
            '''
            Create empty object as control points for the human model
            '''
            # Set the 3D cursor to origin position
            bpy.context.scene.cursor_location = (0, 0, 0)

            bpy.ops.object.mode_set(mode='OBJECT')
            for p in cls.controlPointNames:
                controlEmpty = bpy.data.objects.get(p)
                if not controlEmpty:
                    bpy.ops.object.empty_add(radius=0.05)
                    controlEmpty = bpy.context.object
                    controlEmpty.name = p

        def __init__(self):
            self.boneName = ''
            self.type = ''
            self.target = ''
            self.parameters = {}

        def apply(self):
            '''
            Apply constraint to connect bone and empty control objects
            '''
            self.constraintName = '%s_%s' % (self.type, self.target)
            model = models.humanModel()
            L.info('Setting up constraint %s, %s' % (self.boneName, self.target))

            bone = model.pose.bones.get(self.boneName)
            if not bone:
                L.error('The bone %s can not be found' % self.boneName)

            c = bone.constraints.get(self.constraintName)
            if c:
                L.info('Constraint already exist')
            else:
                c = bone.constraints.new(self.type)

            targetObject = bpy.data.objects.get(self.target)
            if not targetObject:
                L.error('The target object %s can not be found' % self.target)
            c.target = targetObject

            for k in self.parameters:
                L.debug('Setup parameter %s:%s' % (k, self.parameters[k]))
                if k not in dir(c):
                    L.error('Parameter %s is not valid' % k)
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

    class JointInfo:
        '''
        Utilitis to export joint information from the scene
        '''
        @staticmethod
        def export():
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

            # obj = tenon.obj.get('m_c_1')
            obj = models.humanModel()

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
                joints.append((boneId, JointInfo.world2camera(jointLocation)))
            return joints

        @staticmethod
        def serializeJointInfo(filename, joints):
            '''
            Save joint data to file
            '''
            filename = bpy.path.abspath(os.path.expanduser(filename))
            with open(filename, 'w') as f:
                for j in joints:
                    f.write('%s,%s\n' % (j[0], ','.join([str(v) for v in j[1]])))

        @staticmethod
        def world2camera(location):
            '''
            Map the 3d coordinate to camera coordinate
            This is an excellent reference: http://blender.stackexchange.com/questions/882/how-to-find-image-coordinates-of-the-rendered-vertex
            '''
            import bpy, bpy_extras

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


    class Util:
        def __init__(self):
            pass

        def create_lamps(self):
            # Setup lighting for the scene
            radius = 12
            nLight = 16
            z = 10
            lamps = [tenon.obj.Lamp.create('light%d' % v) for v in range(nLight)]
            for i in range(len(lamps)):
                lamp = lamps[i]

                # Compute the location of light source, put the light evenly
                lampObj = tenon.obj.get(lamp.name)
                lampObj.location = tenon.util.sphere_location(radius, 360.0 / nLight * i, 0)
                lampObj.location[2] += z  # Set the z of the light source

            return lamps

        def setup_scene(self):
            # Create pose constraints
            # The contraint point will be initially put on the 3D cursor
            self.create_constraint()
            lamps = self.create_lamps()
            scene = tenon.util.dictwrapper(lamps = lamps)

            return scene

        def update_scene(self, posefolder, scene, poseid):
            import random
            # Update human pose
            # self.animate(os.path.join(self.rootdir, 'data', '2015101415_v2/%04d.csv' % poseid))
            self.animate(os.path.join(posefolder, '%04d.csv' % poseid))

            # Randomly update lighting
            for l in scene.lamps:
                l.energy = random.gauss(1, 1.5)

        def create_constraint(self):
            '''
            Create constraints to animate the human model
            '''
            Constraint.setup()

        def animate(self, posefile):
            '''
            Animate the armature with a pose file
            '''
            # Make the retarget code here.
            # Load data from exported csv file
            loc = Retarget.readJointLocCSV(posefile)
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
                L.debug('Move %s to %s' % (jointName, str(pt)))

                controlEmpty.location.x = pt.x
                controlEmpty.location.y = pt.y
                controlEmpty.location.z = pt.z

            bpy.context.scene.update()  # This is super important

        def render_scene(self, output_dir, filename_no_ext):
            imgfilename = os.path.join(output_dir, 'imgs/%s.png' % filename_no_ext)
            L.info('Render file to %s', L.prettify_filename(imgfilename))
            tenon.render.write(imgfilename)

            depth_filename = os.path.join(output_dir, 'depth/%s.png' % filename_no_ext)
            tenon.render.DepthMode.enable()
            tenon.render.write(depth_filename)
            tenon.render.DepthMode.disable()

            paint_filename = os.path.join(output_dir, 'parts/%s.png' % filename_no_ext)
            tenon.render.PaintMode.enable(models.humanModel())
            tenon.render.write(paint_filename)

            # Also save the joint annotation and part annotation
            joint_filename = os.path.join(output_dir, 'joints/%s.csv' % filename_no_ext)
            joints = JointInfo.export()
            JointInfo.serializeJointInfo(joint_filename, joints)
