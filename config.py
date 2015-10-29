# Define global variables for this project.
RENDER_OUTPUT_DIR = '/q/cache/render_output/'

def bpyPathHelper(relpath):
    # Convert blender relpath to something accessible to other code
    try:
        import bpy
        path = bpy.path.abspath(relpath)
    except:
        import os
        folders = ['scenes', '../scenes'] # depends on where I execute the script
        rootFolders = [v for v in folders if os.path.isdir(v)]

        path = relpath.replace('//', rootFolders[0] + '/')
    return path
    
