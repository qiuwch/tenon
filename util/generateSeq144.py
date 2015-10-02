from datetime import datetime
import random

import sys
sys.path.append('..')
from task import Task, Job
import config


def generateSeq144():
    ''' Generate BVH Sequence 144_43, All types of clothes, Randomly pick a background '''

    clothes = config.getClothList()
    nCloth = len(clothes)
    bgs = config.getBGList()
    nBG = len(bgs)
    print 'Number of clothes: %d, background: %d' % (nCloth, nBG)

    # Number of frames defined in the bvh file
    nFrame = 935
    print 'Number of poses: %d' % nFrame

    now = datetime.now()

    tasks = []

    for iframe in range(nFrame):
        task = Task()
        task.clothId = random.randrange(0, nCloth)
        task.frameId = iframe
        task.backgroundId = random.randrange(0, nBG) # Pick from uniform
        task.mode = 'ipjd' # See definition
        tasks.append(task)

    j = Job()
    j.name = 'ClothParsing'
    j.date = '%02d.%02d' % (now.month, now.day)
    j.comment = 'This is the first batch task definition'
    j.outputFolder = '/q/cache/clothParsing'
    j.tasks = tasks
    j.save(config.pathHelper('//%02d.%02d_Seq144.csv' % (now.month, now.day)))

if __name__ == '__main__':
    generateSeq144() # If run idenpendently, this script and be used to generate the task list
