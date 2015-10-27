# Define global variables for this project.
RENDER_OUTPUT_DIR = '/q/cache/render_output/'
lspJointFile = '/q/cache/lsp_2d_3d/joint_3d/2015101415_v2/%04d.csv' # This is unnormalized version

def bpyPathHelper(relpath):
    # Convert blender relpath to something accessible to other code
    try:
        import bpy
        path = bpy.path.abspath(relpath)
    except:
        path = relpath.replace('//', '../scenes/')
    return path
    
