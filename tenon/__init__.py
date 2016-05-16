import sys, os, subprocess
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
        import tenon.logging as L
        blender = tenon.setting.blender
        # cmd = '%s %s --background --python %s > /dev/null 2>&1' % (blender, scenefile, taskfile)
        cmd = '%s %s --background --python %s >> blender_stdout.log' % (blender, scenefile, taskfile)

        # Redirect the output of blender. The default output is not very useful
        L.info('Start tenon on scene file %s', 'file://%s' % os.path.abspath(scenefile))
        print(cmd)
        os.system(cmd)
        # subprocess.Popen([blender, scenefile, '--background', '--python', taskfile])
