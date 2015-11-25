# Define blender utilities
import bpy

def pm(mat):
	''' Pretty print of matrix '''
	for row in range(4):
		print(','.join(['%6.3f' % v for v in mat[row]]))

def selectedPoseBone():
	return bpy.context.selected_pose_bones[0]

def showMatrix():
	''' Show internal data on the UI for debug purpose '''


# Below code are from the display_matrix plugin
# ---------------------------------------------
from bpy_extras.view3d_utils import location_3d_to_region_2d
import blf

OFFSET_X = 0
OFFSET_Y = 15
FLOAT_FMT = "%.3F"

def draw_text_array(context, vector, texts):
    loc_x, loc_y = location_3d_to_region_2d(
        context.region,
        context.space_data.region_3d,
        vector)
    loc_x += OFFSET_X

    for title, data in texts:
        blf.position(0, loc_x, loc_y, 0)
        blf.draw(0, title)
        loc_y -= OFFSET_Y
        for d in data:
            blf.position(0, loc_x + OFFSET_X, loc_y, 0)
            blf.draw(0, d)
            loc_y -= OFFSET_Y
        loc_y -= OFFSET_Y / 2

def draw_pbone_matrices(context, obj, pbone):
    dm = context.window_manager.display_matrix
    pbone_location_world = pbone.matrix.to_translation()
    for p in pbone.parent_recursive:
        pbone_location_world = p.matrix_basis * pbone_location_world
    pbone_location_world = obj.matrix_world * pbone_location_world

    texts = []

    if dm.show_matrix_pbone_world:
        texts.append(("Matrix:",
                      [", ".join([FLOAT_FMT % n for n in vec])
                       for vec in pbone.matrix]))
    if dm.show_matrix_pbone_basis:
        texts.append(("Matrix Basis:",
                      [", ".join([FLOAT_FMT % n for n in vec])
                       for vec in pbone.matrix_basis]))
    if dm.show_matrix_pbone_channel:
        texts.append(("Matrix Channel:",
                      [", ".join([FLOAT_FMT % n for n in vec])
                       for vec in pbone.matrix_channel]))

    draw_text_array(context, pbone_location_world, texts) 

def draw_matrix_callback(context):
    if context.window_manager.display_matrix.enabled:
        for obj in context.selected_objects:
            draw_matrices(context, obj)


def draw_matrices(context, obj):
    dm = context.window_manager.display_matrix
    mode = obj.mode

    texts = []

    if mode == 'POSE' and dm.show_matrix_pbone:
        if context.selected_pose_bones:
            for pbone in context.selected_pose_bones:
                draw_pbone_matrices(context, obj, pbone)

    elif mode == 'OBJECT' and dm.show_matrix_obj:
        if dm.show_matrix_obj_basis:
            texts.append(("Matrix Basis:",
                          [", ".join([FLOAT_FMT % n for n in vec])
                           for vec in obj.matrix_basis]))
        if dm.show_matrix_obj_local:
            texts.append(("Matrix Local:",
                          [", ".join([FLOAT_FMT % n for n in vec])
                           for vec in obj.matrix_local]))
        if dm.show_matrix_obj_pinverse:
            texts.append(("Matrix Parent Inverse:",
                          [", ".join([FLOAT_FMT % n for n in vec])
                           for vec in obj.matrix_parent_inverse]))
        if dm.show_matrix_obj_world:
            texts.append(("Matrix World:",
                          [", ".join([FLOAT_FMT % n for n in vec])
                           for vec in obj.matrix_world]))

    draw_text_array(context, obj.location, texts)
