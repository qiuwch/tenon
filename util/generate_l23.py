# Task should be able to serialize to files and read from file.
# For each task should define the variables related to this task
import sys
sys.path += ['../..', '..']
from tenon.scene import Bg, Shirt, Pants
from tenon.tasks.l23 import L23Job, L23Task
from tenon.config import bpyPathHelper

from datetime import datetime
import copy
import random
import logging

class ObjectDict(dict):
    def __getattr__(self, key):
        # if key in self:
        return self[key]
        # return None

    def __setattr__(self, key, value):
        self[key] = value


def generate():
    now = datetime.now();
    jobInfo = ObjectDict({
        'name': 'LSP2D3D',
        'shirtFolder': '//textures/cloth/color/',
        'pantsFolder': '//textures/cloth/lower/',
        'filename': '//%s_%02d.%02d.csv' % (L23Job.__name__, now.month, now.day),
        'bgFolder': '//background/INRIA/',
        'outputFolder': '/q/cache/lsp_2d_3d/render_output/',
        'comment': 'Use 2D joint annotation of LSP to manipulate human model',
        'mode': 'ijd'
    })

    j = L23Job()
    for k in jobInfo:
        setattr(j, k, jobInfo[k])

    defTask = L23Task() # Default task
    defTask.mode = jobInfo.mode

    tasks = []

    Shirt.setFolder(j.shirtFolder)
    nShirt = len(Shirt.textures)

    Pants.setFolder(j.pantsFolder)
    nShirt = len(Pants.textures)

    Bg.setFolder(j.bgFolder)
    nBG = len(Bg.textures)

    for i in range(1, 2001):
        t = copy.copy(defTask)
        t.LSPPoseId = i
        t.pantsId = random.randrange(0, nShirt)
        t.bgId = random.randrange(0, nBG)
        t.tshirtId = random.randrange(0, nShirt)
        tasks.append(t)

    j.tasks = tasks
    j.save(bpyPathHelper(j.filename))

if __name__ == '__main__':
    FORMAT = "[%(levelname)s : %(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    generate() 
