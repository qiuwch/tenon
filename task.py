# Script to batch run tasks defined in a data file.

# What kind of variables I need to tweak in the batch mode?

'''
1. Lighting
2. Pose
3. Camera (view angle)
4. Cloth
5. Occlusion?
6. Blur, out of focus?
'''

# It is annoying that I can not use pandas in my project.

import pandas as pd
import bpy
import tenon.background
import tenon.animate
from tenon.render import render

def testTask():
	df = pd.read_csv(bpy.path.abspath('//task.csv'))
	print(df.rowId)

	# For each task defined in the task. Configure the scene.

class Task:
	def __init__(self):
		pass

def run():
	df = pd.read_csv(bpy.path.abspath('//task.csv'))
	num = len(df)

	for i in range(num):
		t = Task()
		t.rowId = df.rowId[i]
		t.backgroundId = df.backgroundId[i]
		t.frameId = df.frameId[i]
		t.clothId = df.clothId[i]
		doTask(t)

def doTask(t):
	tenon.background.setINRIA(t.backgroundId)

	# joints = tenon.animate.toFrame(t.frameId);
	prefix = 'im%04d' % (t.rowId+1) # Let it start from 1

	render.realisticMode()
	render.write(render.outputFolder + '/imgs/' + prefix + '.png')

	render.depthMode()
	render.write(render.outputFolder + '/depth/' + prefix + '.png')
