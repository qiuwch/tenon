# Task should be able to serialize to files and read from file.
# For each task should define the variables related to this task
import sys
sys.path.append('..')

from datetime import datetime
import copy
from task import LSP3Dtask, Job



def generate():
    defTask = LSP3Dtask()
    defTask.mode = 'ijd'

    tasks = []

    # Fix cloth, random background, for each pose
    for i in range(1, 2001):
        t = copy.copy(defTask)
        t.LSPPoseId = i
        tasks.append(t)

    j = Job()
    j.name = 'LSP2D3D'
    now = datetime.now(); j.date = '%02d.%02d' % (now.month, now.day)
    j.comment = 'Use 2D joint annotation of LSP to manipulate human model'
    j.outputFolder = '/q/cache/lsp_2d_3d/render_output/'
    j.tasks = tasks
    j.save('../scenes/%02d.%02d_lsp2to3.csv' % (now.month, now.day))

if __name__ == '__main__':
    generate() 





# class MocapTask(Task):
# 	def __init__(self):
# 		Task.__init__(self)
# 		self.PROP_LIST += ['backgroundId', 'frameId', 'clothId']
