
import os

PREFIX = os.environ.get('CONDA_PREFIX')


QTDIR=PREFIX
QT4_FRAMEWORK=False

python_includes=PREFIX+"/include/python2.7"
python_libpath=PREFIX+"/lib"
boost_includes=PREFIX+"/include"
boost_lib=PREFIX+"/lib"
openalea_lib=PREFIX+"/lib"
openalea_includes=PREFIX+"/include"
plantgl_lib=PREFIX+'/build-scons/lib'
plantgl_include=PREFIX+'/src/cpp'

