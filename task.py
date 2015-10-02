# Script to batch run tasks defined in a data file.
# TODO: Consider rewriting it with protobuf
class Job:
    requiredProp = [ # Required properties
        'name',
        'date',
        'outputFolder', 
        # TODO: Check consistency, 'blendFile',
    ]

    def __init__(self):
        pass

    def validate(self):
        # Check whether this is a valid job
        for prop in Job.requiredProp: # Make sure this file is valid
            assert(prop in dir(self))

        assert(len(self.tasks) != 0)

    def save(self, filename):
        self.validate()

        with open(filename, 'w') as f:
            for prop in dir(self):
                if prop[0] != '_' and type(getattr(self, prop)) == str:
                    line = '%s : %s' % (prop, getattr(self, prop))
                    f.write(line + '\n')

            f.write(Task.header() + '\n')
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

            while line.strip() == '':
                line = f.readline() # Skip empty line

            # Read task list from file
            headerLine = line
            assert(headerLine.strip() == ','.join(Task.PROP_LIST))

            line = f.readline()
            while line:
                t = Task()
                t.parseFromLine(line)
                tasks.append(t)
                line = f.readline()

            j.tasks = tasks

        j.validate()

        return j

    def run(self, limit=None):
        count = 0 # Number of generated images
        # Execute task
        for t in self.tasks:
            t.execute(self.outputFolder)

            count += 1
            if limit and count >= limit:  # Limit the number of generation, handy for debug
                break

class Task:
    PROP_LIST = [
        'rowId',
        'backgroundId',
        'frameId',
        'clothId',
        'mode' # i:image, j:joint, d:depth, p:part
    ]
    def __init__(self):
        pass

    @classmethod
    def header(cls):
        return ','.join(Task.PROP_LIST)

    def parseFromLine(self, line):
        cols = line.split(',')
        for i in range(len(Task.PROP_LIST)):
            setattr(self, Task.PROP_LIST[i], cols[i])
        self.frameId = int(self.frameId) # Explict conversion
        self.rowId = int(self.rowId)
        self.clothId = int(self.clothId)
        self.backgroundId = int(self.backgroundId)

    def serilizeToLine(self):
        cols = [str(getattr(self, v)) for v in Task.PROP_LIST]
        line = ','.join(cols)
        return line

    def execute(self, outputFolder):
        # TODO: timing this script to boost speed
        self.outputFolder = outputFolder

        self.prefix = 'im%04d' % (self.rowId) # Let it start from 1

        self.setPose()
        self.setCloth()
        self.setBackground()

        self.render()


    def render(self):
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
            self.serializeJointInfo(self.outputFolder + '/joint' + self.prefix + '.csv', joints)

    def serializeJointInfo(self, filename, joints):
        import os
        folder = os.path.split(filename)[0]
        print(folder)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(filename, 'w') as f:
            for j in joints:
                f.write('%s,%s\n' % (j[0], ','.join([str(v) for v in j[1]])))


    def setPose(self):
        import tenon.animate # TODO: check speed issue
        joints = tenon.animate.toFrame(self.frameId)
        self.pose = joints

    def setCloth(self): # The protocol of setting cloth
        import tenon.cloth
        tenon.cloth.changeClothById(tenon.cloth.ClothType.TShirt, self.clothId)

    def setBackground(self): # The protocol of setting background
        import tenon.background
        tenon.background.setINRIA(self.backgroundId)

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
        print('%d: %s' % (ii, csvFiles[ii]))
        print('Name:%s, Date:%s, Num:%d' % (j.name, j.date, len(j.tasks)))
        
        js.append(j)
    return js


if __name__ == '__main__':
    # Run a unit test here
    ls()
