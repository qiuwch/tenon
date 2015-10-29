import os
blender = '/Applications/blender.app/Contents/MacOS/blender'
task = [
	['scenes/m_c_1.blend', 'run.py'],
	['scenes/m_c_2.blend', 'run.py'],
	['scenes/m_c_3.blend', 'run.py'],
	['scenes/f_c_1.blend', 'run.py'],
	['scenes/f_c_2.blend', 'run.py'],
	['scenes/f_c_3.blend', 'run.py'],
]

for t in task:
	cmd = '%s %s --background --python %s' % (blender, t[0], t[1])
	print(cmd)
	os.system(cmd)
