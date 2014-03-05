# -*- coding: utf-8 -*-
__revision__ = "$Id$"

from setuptools import setup, find_packages
import os, sys
from os.path import join as pj


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


## compile cython code
cwd = os.getcwd()
os.chdir('src/stocatree')
os.system('python build_cython.py')
os.chdir(cwd)

if __name__ == '__main__':

    setup(name=name,
          version=version,
          author=authors,
          author_email=authors_email,
          description=description,
          url=url,
          license=license,

          namespace_packages=['vplants'],
          create_namespaces=True,

          # Packages
          packages=['openalea', 'openalea.stocatree',
                    'vplants.stocatree',],

          package_dir={'vplants.stocatree' : 'src/stocatree',
                       '' : 'src', # hack to use develop command
                       },

          package_data = {'' : ['*.lpy', '*.fset', '*.s' ,'*.txt', '*pyd', '*.so'],},
          include_package_data = True,
          share_dirs = {'share':'share'},
          # Add package platform libraries if any
          zip_safe = False,

          # Dependencies
          install_requires = ['vplants.plantgl', 'cython', 'lockfile'],
          dependency_links = ['http://openalea.gforge.inria.fr/pi'],
          #cmdclass={'build_ext':build_ext},
          #ext_modules = ext_modules,

          entry_points = {
            "wralea": [ "openalea.stocatree = stocatree_wralea",
                        "openalea.stocatree.configuration = stocatree_configuration_wralea",
            ]
            },



          )



