from datetime import datetime
import random
import copy

import sys
sys.path.append('..')
from task import Task, Job
import config

def generateFixFactor():
    ''' Change factor one at a time, to see the changing of performance '''

    clothes = config.getClothList()
    nCloth = len(clothes)
    bgs = config.getBGList()
    nBG = len(bgs)
    print 'Number of clothes: %d, background: %d' % (nCloth, nBG)

    nFrame = 935


    defTask = Task()
    defTask.clothId = 0
    defTask.frameId = 0
    defTask.backgroundId = 0
    defTask.mode = 'ipjd'

    now = datetime.now()

    tasks = []
    # Fix cloth, random background, for each pose
    for iframe in range(nFrame):
        for clothId in range(5):
            t = copy.copy(defTask)
            t.frameId = iframe
            t.clothId = clothId
            t.backgroundId = random.randrange(0, nBG)
            tasks.append(t)

    # Fix background, random cloth
    for iframe in range(nFrame):
        for backgroundId in range(5):
            t = copy.copy(defTask)
            t.frameId = iframe
            t.backgroundId = backgroundId
            t.clothId = random.randrange(0, nCloth)
            tasks.append(t)

    j = Job()
    j.name = 'FixFactor'
    j.date = '%02d.%02d' % (now.month, now.day)
    j.comment = 'Fix one factor at a time to see the effect'
    j.outputFolder = '/q/cache/fixFactorPose'
    j.tasks = tasks
    j.save(config.pathHelper('//%02d.%02d_fix.csv' % (now.month, now.day)))

if __name__ == '__main__':
    generateFixFactor() 



