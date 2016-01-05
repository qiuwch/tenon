# Demo script to show how to use tenon
import tenon
import sys

if __name__ == '__main__':
    if sys.argv[0].endswith('blender'):
        s = tenon.Scene('')
        s.render()

    if sys.argv[0].endswith('python'):
        tenon.run(s, __file__)

# Define a scene first, then apply scene spefic operation.
