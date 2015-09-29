# Script to load tenon into blender
import sys, imp, re, os

# Space between = is required
PWD = '/Users/qiuwch/Dropbox/Workspace/research/CG/'
sitePkg = '/usr/local/lib/python3.4/site-packages/'

for v in [PWD, sitePkg]:
    sys.path.append(v)

# Add python site packages into blender, so that I can use third party libs.
# TODO: check python version of blender first
print(sys.version) # This is the python version. Do not mix python2 and 3 libs.

def r(v):
    imp.reload(v)

# if __name__ == '__main__':
if '__file__' in globals():
    with open('./init.py') as f:
        data = f.read()
        data = re.sub('PWD = .*', 'PWD = %s' % os.path.abspath('..'), data)
        print(data)
else:
    # Import for the convinience of interactive shell
    import tenon.demo as td
    from tenon.render import render
    from tenon.config import *
    from tenon.bpyutil import *
    import tenon.pose, tenon.export, tenon.task
