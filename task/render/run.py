#!env python
import argparse
import os
import sys
sys.path.append('../../tenon')
import settings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', help = 'Python script which defined the rendering task')
    parser.add_argument('--scene', default='../../scenes/m_c_1.blend', help = 'The blender scene to run on')

    args = parser.parse_args()

    blender = settings.blender
    cmd = '%s %s --background --python %s' % (blender, args.scene, args.task)

    # Redirect the output of blender. The default output is not very useful
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    main()
