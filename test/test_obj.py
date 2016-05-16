# Make sure the log information from tenon would not contaminate here
tenonpath = '..'
import sys; sys.path.append(tenonpath)
import tenon

tenon.run(__file__, '../demo.blend')
if tenon.inblender():
    tenon.obj.get('non_exist_obj')
    # Expected to produce a warning message