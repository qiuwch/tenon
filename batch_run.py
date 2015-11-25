import os
blender = 'blender'
task = [
    ['scenes/m_c_1.blend', 'run.py'],
    ['scenes/m_c_2.blend', 'run.py'],
    ['scenes/m_c_3.blend', 'run.py'],
    ['scenes/f_c_1.blend', 'run.py'],
    ['scenes/f_c_2.blend', 'run.py'],
    ['scenes/f_c_3.blend', 'run.py'],
]


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        i = int(sys.argv[1])
        print('Run task %d' % i)
        ts = [task[i]]
    else:
        ts = task

    for i in range(20):
        for t in ts:
            cmd = '%s %s --background --python %s' % (blender, t[0], t[1])
            print(cmd)
            os.system(cmd)

# Also do the post processing after the rendering automatically
