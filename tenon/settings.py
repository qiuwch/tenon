# This is a dummy file, actual setting is stored in ~/local_settings.py
import sys, os
sys.path.append(os.path.expanduser('~'))
try:
    from local_settings import *
except ImportError as e:
    print('Import local_settings failed')