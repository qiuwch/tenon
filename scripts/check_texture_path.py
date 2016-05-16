# The textures in blender are sometimes referenced by their absolute path. So moving around the blend file will sometimes break the material reference and procude an empty image.

import sys, os, argparse
sys.path.append(os.path.abspath('..')) # define where python can find tenon
import tenon
import tenon.logging as L

def check_texture():
    import bpy, os
    texs = bpy.data.textures
    def check_exist(file):
        return os.path.isfile(file)

    for t in texs:
        L.info('Check texture {}'.format(t))
        if isinstance(t, bpy.types.ImageTexture) and t.image.source == 'FILE':

            filepath = bpy.path.abspath(t.image.filepath)
            exist = check_exist(filepath)
            L.info('File {} exist {}'.format(t.image.filepath, exist))

''' not useful right now
searchstr = '/home/qiuwch/Dropbox/workspace/tenon/data/textures/'
newstr = '/home/qiuwch/Dropbox/workspace/graphics_for_vision/tenon/data/textures/'
def replace_texture(searchstr, newstr):
    from os.path import isfile
    texs = bpy.data.textures
    # Fix broken texture file path and replace it as relpath
    for t in texs:
        print('Check texture {}'.format(t))
        if isinstance(t, bpy.types.ImageTexture) and t.image.source == 'FILE':
            exist = isfile(t.image.filepath)
            print('Previous file {} exist {}'.format(t.image.filepath, exist))
            newpath = t.image.filepath.replace(searchstr, newstr)
            print('New file {} exist {}'.format(newpath, isfile(newpath)))

            if not exist and isfile(newpath):
                newpath = bpy.path.relpath(newpath)
                t.image.filepath = newpath
                t.image.reload()
        # t.image.update, t.image.reload?
        # type(t.image) == bpy.types.Image
                print('Replace old path with {}'.format(newpath))
'''

def main():
    check_texture()

if __name__ == '__main__':
    if not tenon.inblender():
        parser = argparse.ArgumentParser()
        parser.add_argument('blendfile')
        args = parser.parse_args()
        tenon.run(__file__, args.blendfile)
    else:
        main()
