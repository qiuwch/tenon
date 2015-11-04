import os
import logging

def strTimeStamp():
    import time
    timeStamp = time.strftime('%Y%m%d%H%M', time.localtime())
    return timeStamp

def serializablePropList(obj):
    public = [v for v in dir(obj) if not v.startswith('__')]
    props = [v for v in public if type(getattr(obj, v)) == str or isinstance(getattr(obj,v), (int, float, complex))]
    return props


class Job:
    requiredProps = [ # Required properties
        'name',
        'outputFolder', 
    ]

    def __init__(self):
        self.tasks = []

    def __str__(self):
        objStr = '\nName:%s, Num:%d\n' % (self.name, len(self.tasks))
        for p in serializablePropList(self.tasks[0]):
            objStr += '%s:%s\n' % (p, getattr(self.tasks[0], p))
        return objStr

    def __repr__(self):
        return self.__str__()

    def validate(self):
        # Check whether this is a valid job
        for prop in self.requiredProps: # Make sure this file is valid
            if not prop in dir(self):
                logging.error('Job: property %s is required but missing.' % prop)

        for t in self.tasks:
            t.validate()

        assert(len(self.tasks) != 0)

    def save(self, filename):
        self.validate()

        with open(filename, 'w') as f:
            taskInstance = self.tasks[0]
            self.tasktype = taskInstance.__class__.__name__
            # Be aware: this is black tech of python, cautious of malware input
            # for prop in dir(self):
            for prop in serializablePropList(self):
                # if not prop[0].startswith('__') and type(getattr(self, prop)) == str:
                line = '%s : %s' % (prop, getattr(self, prop))
                f.write(line + '\n')

            count = 0
            for task in self.tasks:
                task.rowId = count
                count += 1


            f.write(taskInstance.header() + '\n')
            for task in self.tasks:
                line = task.serilizeToLine()
                f.write(line + '\n')

    def logOn(self):
        # Set up python logging to direct all logging to the output folder
        timeStamp = strTimeStamp()
        logFile = self.outputFolder + timeStamp + 'info.txt'
        fh = logging.FileHandler(logFile)
        fh.setLevel(logging.INFO)

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # fh.setFormatter(formatter)
        logging.root.addHandler(fh)
        self._fh = fh

    def logOff(self):
        # Disable python logging
        # Saving log of this job
        if self._fh and self._fh in logging.root.handlers:
            logging.root.handlers.removeHandler(self._fh)


    def run(self, limit=None):
        self.setupScene() 
        # The information of this job can be modified here
        # Do real job after setupScene()

        # Create output folder
        if not os.path.isdir(self.outputFolder):
            os.mkdir(self.outputFolder)

        # Enable log and write log file to output folder
        self.logOn()
        import tenon.info
        logging.info(tenon.info.cameraInfo())
        logging.info(tenon.info.blendInfo())

        count = 0 # Number of generated images
        # Execute task
        for t in self.tasks:
            t.outputFolder = self.outputFolder
            t.execute()

            count += 1
            if limit and count >= limit:  # Limit the number of generation, handy for debug
                break

        self.logOff()

class Task:
    requiredProps = [
        # 'rowId', # This is an automatic field
        'mode' # i:image, j:joint, d:depth, p:part
    ]

    def __init__(self):
        self.mode = 'ipjd'

    def header(self):
        headerLine = ','.join(serializablePropList(self))
        logging.debug('Header of type %s is %s' % (self.__class__.__name__, headerLine))
        return headerLine

    def parseFromLine(self, line, header):
        cols = line.strip().split(',')
        if not len(header) == len(cols):
            logging.error('Error when parsing line %s, the required fields are %s' % (line, header))

        for i in range(len(header)):
            setattr(self, header[i], cols[i])

    def validate(self):
        for prop in self.requiredProps:
            if not prop in dir(self):
                logging.error('Task: property %s is required but missing.' % prop)

    def serilizeToLine(self):
        cols = [str(getattr(self, v)) for v in serializablePropList(self)]
        line = ','.join(cols)
        return line

    def isRendered(self):
        mapping = {
            'i': ['imgs', 'png'],
            'd': ['depth', 'png'],
            'p': ['paint', 'png'],
            'j': ['joint', 'csv']
        }

        isRendered = True
        for k in mapping.keys():
            v = mapping[k]
            filename = '%s/%s/%s.%s' % (self.outputFolder, v[0], self.prefix, v[1])
            if k in self.mode and not os.path.isfile(filename):
                isRendered = False

        return isRendered


    def render(self):
        ''' Share between task types '''
        from tenon.render import Render

        if 'i' in self.mode:
            Render.realisticMode()
            Render.write(self.outputFolder + '/imgs/' + self.prefix + '.png')

        if 'd' in self.mode:
            Render.depthModeOn()
            Render.write(self.outputFolder + '/depth/' + self.prefix + '.png')
            Render.depthModeOff()

        if 'p' in self.mode:
            Render.paintModeOn()
            Render.write(self.outputFolder + '/paint/' + self.prefix + '.png')
            Render.paintModeOff()

        if 'j' in self.mode:
            # Write joint annotation to a final csv file
            joints = Render.exportJoint()
            self.serializeJointInfo(self.outputFolder + '/joint/' + self.prefix + '.csv', joints)

    def serializeJointInfo(self, filename, joints):
        import os
        folder = os.path.split(filename)[0]

        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(filename, 'w') as f:
            for j in joints:
                f.write('%s,%s\n' % (j[0], ','.join([str(v) for v in j[1]])))
