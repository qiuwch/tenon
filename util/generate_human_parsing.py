import sys
sys.path.append('../..')

from datetime import datetime
import random
from tenon.task import HumanParsingTask, Job
import tenon.cloth, tenon.background



def generateSeq144():
    ''' Generate BVH Sequence 144_43, All types of clothes, Randomly pick a background '''
    j = Job()

    j.clothFolder = '//textures/cloth/upper/' # It seems blender is not good at handling . and ..
    tenon.cloth.setClothFolder(j.clothFolder)
    nCloth = len(tenon.cloth.clothTextures)

    j.pantsFolder = '//textures/cloth/lower/' # It seems blender is not good at handling . and ..
    tenon.cloth.setPantsFolder(j.pantsFolder)
    nPant = len(tenon.cloth.pantsTextures)

    j.bgFolder = '//background/INRIA/'
    tenon.background.setBGFolder(j.bgFolder)
    nBG = len(tenon.background.bgFiles)

    print 'Number of clothes: %d, background: %d' % (nCloth, nBG)

    # Number of frames defined in the bvh file
    nFrame = 935
    print 'Number of poses: %d' % nFrame

    now = datetime.now()

    tasks = []

    for iframe in range(nFrame):
        task = HumanParsingTask()
        task.clothId = random.randrange(0, nCloth)
        task.pantId = random.randrange(0, nPant)
        task.frameId = iframe
        task.backgroundId = random.randrange(0, nBG) # Pick from uniform
        task.mode = 'ipjd' # See definition
        tasks.append(task)

    j.name = 'Human Parsing'
    j.date = '%02d.%02d' % (now.month, now.day)
    j.comment = 'This is the first batch task definition'
    j.outputFolder = '/q/cache/human_parsing/'
    j.tasks = tasks
    j.save('../scenes/%02d.%02d_human_parsing.csv' % (now.month, now.day))

class HumanParsingTask(Task):
    PROP_LIST = Task.PROP_LIST + ['backgroundId', 'frameId', 'clothId', 'pantId']

    def __init__(self):
        Task.__init__(self)

    def execute(self):
        # TODO: timing this script to boost speed
        self.prefix = 'im%04d' % (int(self.rowId) + 1) # TODO: Let it start from 1
        outputFile = '%s/%s.png' % (self.outputFolder, self.prefix)
        if os.path.isfile(outputFile):
            logging.info('Skip render exist file %s' % outputFile)
            pass

        self.setPose()
        self.setCloth()
        self.setPant()
        self.setBackground()

        self.render()

    def setPose(self):
        import tenon.animate # TODO: check speed issue
        joints = tenon.animate.toFrame(int(self.frameId))
        self.pose = joints


if __name__ == '__main__':
    generateSeq144() # If run idenpendently, this script and be used to generate the task list
