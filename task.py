# Script to batch run tasks defined in a data file.
# TODO: Consider rewriting it with protobuf
import os

def strTimeStamp():
    import time
    timeStamp = time.strftime('%Y%m%d%H%M', time.localtime())
    return timeStamp

def getStrPropList(obj):
    return [v for v in dir(obj) if not v.startswith('__') and type(getattr(obj, v)) == str]

def info(msg): # Use this to differentiate debug info with useful info
    print(msg)

class Job:
    requiredProp = [ # Required properties
        'name',
        'date',
        'outputFolder', 
        'clothFolder',
        'bgFolder',
        # TODO: Check consistency, 'blendFile',
    ]

    def __str__(self):
        objStr = ''
        objStr += 'Name:%s, Date:%s, Num:%d\n' % (self.name, self.date, len(self.tasks))
        for p in getStrPropList(self.tasks[0]):
            objStr += '%s:%s\n' % (p, getattr(self.tasks[0], p))
        return objStr

    def __repr__(self):
        return self.__str__()


    def __init__(self):
        pass

    def validate(self):
        # Check whether this is a valid job
        for prop in Job.requiredProp: # Make sure this file is valid
            assert prop in dir(self), 'Job: property %s is required but missing.' % prop

        assert(len(self.tasks) != 0)

    def save(self, filename):
        self.validate()

        with open(filename, 'w') as f:
            taskInstance = self.tasks[0]
            self.tasktype = taskInstance.__class__.__name__
            # Be aware: this is black tech of python, cautious of malware input
            # for prop in dir(self):
            for prop in getStrPropList(self):
                # if not prop[0].startswith('__') and type(getattr(self, prop)) == str:
                line = '%s : %s' % (prop, getattr(self, prop))
                f.write(line + '\n')

            f.write(taskInstance.header() + '\n')
            count = 0
            for task in self.tasks:
                task.rowId = count
                line = task.serilizeToLine()
                f.write(line + '\n')
                count += 1


    @staticmethod
    def parseFromFile(filename):
        ''' Read task from csv file, each row corresponds to a task '''
        j = Job()
        tasks = []

        with open(filename) as f:
            # Read header from file
            line = f.readline()
            sep = line.find(':')
            while sep != -1:
                header = line[:sep].strip()
                content = line[sep+1:].strip()
                setattr(j, header, content)
                line = f.readline()
                sep = line.find(':')

            # print(j.tasktype)
            assert(j.tasktype != None and j.tasktype != "")
            taskClass = eval(j.tasktype)

            j.outputFolder += '/%s/' % strTimeStamp() # Put into a subfolder with timestamp
            while line.strip() == '':
                line = f.readline() # Skip empty line

            # Read task list from file
            headerLine = line
            # print headerLine.strip()
            # print ','.join(taskClass.PROP_LIST)

            assert set(headerLine.strip().split(',')) == set(taskClass.PROP_LIST), '%s not equal %s' % (headerLine, str(taskClass.PROP_LIST))

            ordered_PROP_LIST = headerLine.strip().split(',')
            # Use the order defined in task file

            line = f.readline()
            while line:
                t = taskClass()
                t.PROP_LIST = ordered_PROP_LIST
                t.parseFromLine(line)
                t.outputFolder = j.outputFolder
                tasks.append(t)
                line = f.readline()

            j.tasks = tasks

        j.validate()

        return j

    def run(self, limit=None):
        if not os.path.isdir(self.outputFolder):
            os.mkdir(self.outputFolder)

        import tenon.info
        timeStamp = strTimeStamp()

        logger = tenon.info.Logger(self.outputFolder + timeStamp + 'info.txt')
        logger.info(tenon.info.cameraInfo())
        logger.info(tenon.info.blendInfo())

        # Set the environment
        import tenon.cloth
        tenon.cloth.setClothFolder(self.clothFolder)

        if getattr(self, 'pantsFolder'):
            tenon.cloth.setPantsFolder(self.pantsFolder)

        import tenon.background
        tenon.background.setBGFolder(self.bgFolder)

        count = 0 # Number of generated images
        # Execute task
        for t in self.tasks:
            t.execute()

            count += 1
            if limit and count >= limit:  # Limit the number of generation, handy for debug
                break

class Task:
    # PROP_LIST = [
    #     'rowId',
    #     'backgroundId',
    #     'frameId',
    #     'clothId',
    #     'mode' # i:image, j:joint, d:depth, p:part
    # ]
    PROP_LIST = [
        'rowId',
        'mode'
    ]
    def __init__(self):
        self.mode = 'ipjd'

    def header(self):
        return ','.join(self.PROP_LIST)

    def parseFromLine(self, line):
        cols = line.strip().split(',')
        for i in range(len(self.PROP_LIST)):
            setattr(self, self.PROP_LIST[i], cols[i])
        # self.frameId = int(self.frameId) # Explict conversion
        # self.rowId = int(self.rowId)
        # self.clothId = int(self.clothId)
        # self.backgroundId = int(self.backgroundId)

    def serilizeToLine(self):
        cols = [str(getattr(self, v)) for v in self.PROP_LIST]
        line = ','.join(cols)
        return line




    def render(self):
        ''' Share between task types '''
        from tenon.render import render

        if 'i' in self.mode:
            render.realisticMode()
            render.write(self.outputFolder + '/imgs/' + self.prefix + '.png')

        if 'd' in self.mode:
            render.depthModeOn()
            render.write(self.outputFolder + '/depth/' + self.prefix + '.png')
            render.depthModeOff()

        if 'p' in self.mode:
            render.paintModeOn()
            render.write(self.outputFolder + '/paint/' + self.prefix + '.png')
            render.paintModeOff()

        if 'j' in self.mode:
            # Write joint annotation to a final csv file
            joints = render.exportJoint()
            self.serializeJointInfo(self.outputFolder + '/joint/' + self.prefix + '.csv', joints)

    def serializeJointInfo(self, filename, joints):
        import os
        folder = os.path.split(filename)[0]

        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(filename, 'w') as f:
            for j in joints:
                f.write('%s,%s\n' % (j[0], ','.join([str(v) for v in j[1]])))

    def setCloth(self): # The protocol of setting cloth
        import tenon.cloth
        tenon.cloth.changeClothById(tenon.cloth.ClothType.TShirt, int(self.clothId))

    def setPant(self):
        import tenon.cloth
        tenon.cloth.changeClothById(tenon.cloth.ClothType.Short, int(self.pantId))  # TODO: this is a quick hack, fix this later.

    def setBackground(self): # The protocol of setting background
        import tenon.background
        tenon.background.changeBGbyId(int(self.backgroundId))

class LSP3Dtask(Task):
    PROP_LIST = Task.PROP_LIST + ['LSPPoseId', 'clothId', 'backgroundId']
    def __init__(self):
        Task.__init__(self)
        # Define the property list for this task

    def setPose(self):
        print('Animate to Pose %d' % int(self.LSPPoseId))
        import tenon.puppet
        tenon.puppet.animateCP(int(self.LSPPoseId))
        # tenon.pose.animateEditBone(int(self.LSPPoseId))
        # This is for debugging

    def execute(self):
        # TODO: timing this script to boost speed
        self.prefix = 'im%04d' % (int(self.rowId) + 1) # TODO: Let it start from 1

        self.setPose()
        self.setCloth()
        self.setBackground()

        self.render()

class HumanParsingTask(Task):
    PROP_LIST = Task.PROP_LIST + ['backgroundId', 'frameId', 'clothId', 'pantId']

    def __init__(self):
        Task.__init__(self)

    def execute(self):
        # TODO: timing this script to boost speed
        self.prefix = 'im%04d' % (int(self.rowId) + 1) # TODO: Let it start from 1

        self.setPose()
        self.setCloth()
        self.setPant()
        self.setBackground()

        self.render()

    def setPose(self):
        import tenon.animate # TODO: check speed issue
        joints = tenon.animate.toFrame(int(self.frameId))
        self.pose = joints



class MocapTask(Task):
    PROP_LIST = Task.PROP_LIST + ['backgroundId', 'frameId', 'clothId']

    def __init__(self):
        Task.__init__(self)

    def execute(self):
        # TODO: timing this script to boost speed
        self.prefix = 'im%04d' % (int(self.rowId) + 1) # TODO: Let it start from 1

        self.setPose()
        self.setCloth()
        self.setBackground()

        self.render()

    def setPose(self):
        import tenon.animate # TODO: check speed issue
        joints = tenon.animate.toFrame(int(self.frameId))
        self.pose = joints




def ls():
    ''' Utility to list all available task '''
    import glob

    try:
        import bpy
        fmt = bpy.path.abspath('//*.csv')
    except:
        fmt = './scenes/*.csv'

    csvFiles = glob.glob(fmt) # TODO: fix path helper

    js = []
    for ii in range(len(csvFiles)):
        csvFile = csvFiles[ii]
        j = Job.parseFromFile(csvFile)
        info('%d: %s' % (ii, csvFiles[ii]))
        info(str(j))
        
        js.append(j)
    return js


if __name__ == '__main__':
    # Run a unit test here
    ls()
