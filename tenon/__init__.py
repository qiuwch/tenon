import sys, os
# import tenon # What will happen if I do this loop import?
import tenon.setting # preload of module

def inblender():
    if sys.argv[0].endswith('blender'):
        return True
    else:
        return False

if inblender():
    import tenon.obj
    import tenon.render
    import tenon.logging
    import tenon.util
    import mathutils # ? TODO

def run(taskfile, scenefile):
    if not tenon.inblender():
        blender = tenon.setting.blender
        cmd = '%s %s --background --python %s' % (blender, scenefile, taskfile)

        # Redirect the output of blender. The default output is not very useful
        print(cmd)
        os.system(cmd)
