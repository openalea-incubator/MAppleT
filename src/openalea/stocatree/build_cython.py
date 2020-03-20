import sys
import os

if("win32" in sys.platform):
    os.system('python setup.py build_ext --compiler=mingw32 --inplace')
else:
    os.system('python setup.py build_ext --inplace')



