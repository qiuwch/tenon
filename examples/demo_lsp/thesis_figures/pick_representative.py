import os

fs = [5, 9, 15, 17, 19, 26, 50, 59, 62, 65, 67, 71, 73, 78, 81, 82, 83, 89]

for f in fs:
    cmd = 'cp compare/%d.png pick/%d.png' % (f, f)
    os.system(cmd)