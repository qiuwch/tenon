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
# import pandas as pd # No need anymore


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

    def serilizeToLine(self):
        cols = [str(getattr(self, v)) for v in Task.PROP_LIST]
        line = ','.join(cols)
        return line

    def execute(self, outputFolder):
        # TODO: timing this script to boost speed
        self.outputFolder = outputFolder
        self.prefix = 'im%04d' % (self.rowId+1) # Let it start from 1

        self.setPose()
        self.setCloth()
        self.setBackground()

        self.render()


    def render(self):
        if 'i' in self.mode:
            render.realisticMode()
            render.write(self.outputFolder + '/imgs/' + self.prefix + '.png')

        if 'd' in self.mode:
            render.depthMode()
            render.write(self.outputFolder + '/depth/' + self.prefix + '.png')

        if 'p' in self.mode:
            tenon.paint.humanPaintOn()
            render.write(self.outputFolder + '/paint/' + self.prefix + '.png')

        if 'j' in self.mode:
            # Write joint annotation to a final csv file
            # Save self.pose
            pass

    def setPose(self):
        joints = tenon.animate.toFrame(self.frameId)
        self.pose = joints

    def setCloth(self): # The protocol of setting cloth
        tenon.cloth.changeClothById(tenon.cloth.ClothType.TShirt)

    def setBackground(self): # The protocol of setting background
        tenon.background.setINRIA(self.backgroundId)

def readTaskList(filename):
    ''' Read task from csv file, each row corresponds to a task '''
    tasks = []

    f = open(filename)
    line = f.readline()
    while line:
        t = Task()
        t.parseFromLine(line)
        tasks.append(t)
        line = f.readline()

    f.close()

    return tasks

def run(num = None):
    # Lazy load
    import bpy
    import tenon.background
    import tenon.cloth
    import tenon.animate
    import tenon.paint
    from tenon.render import render

    # Read task list from file
    TASK_FILE = bpy.path.abspath('//task.csv') # TODO: clean this mess
    tasks = readTaskList(TASK_FILE)

    count = 0 # Number of generated images
    # Execute task
    for t in tasks:
        t.execute()

        count += 1
        if num and count > num:  # Limit the number of generation, handy for debug
            break



