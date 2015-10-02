from datetime import datetime
import glob
import random

import sys
sys.path.append('..')
from task import Task

def pathHelper(relpath):
	path = '/Users/qiuwch/Dropbox/Workspace/research/CG/code/tenon/scenes' + relpath
	# path = '..' + relpath
	return path

def getClothList(): # TODO combine this with task execution
    jpgs = glob.glob(pathHelper('//textures/*.jpg'))
    pngs = glob.glob(pathHelper('//textures/*.png'))
    files = jpgs + pngs
    return files

def getBGList():
    BGlist = glob.glob(pathHelper('//background/INRIA/*.jpg'))
    return BGlist

def generateSeq144():
    ''' Generate BVH Sequence 144_43, All types of clothes, Randomly pick a background '''

    # Load cloth list
    clothes = getClothList()
    nCloth = len(clothes)
    print 'Number of clothes: %d' % nCloth

    # Load background list
    bgs = getBGList()
    nBG = len(bgs)
    print 'Number of background: %d' % nBG

    # Number of frames defined in the bvh file
    nFrame = 935
    print 'Number of poses: %d' % nFrame

    now = datetime.now()
    f = open(pathHelper('//%02d.%02d_Seq144.csv' % (now.month, now.day)), 'w')
    f.write(Task.header() + '\n')

    count = 0
    # for ic in range(nCloth):
    for iframe in range(nFrame):
        task = Task()
        task.rowId = count
        # task.clothId = ic
        task.clothId = random.randrange(0, nCloth)
        task.frameId = iframe
        task.backgroundId = random.randrange(0, nBG) # Pick from uniform
        task.mode = 'ipjd' # See definition
        line = task.serilizeToLine()

        f.write(line + '\n')
        count += 1

    f.close()

def generateTask():
    generateSeq144()

if __name__ == '__main__':
    generateTask() # If run idenpendently, this script and be used to generate the task list
