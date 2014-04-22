#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Han
#
# Created:     24/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os

def ensureLocalDir(dir_name):
  d = os.path.join(os.getcwd(), dir_name)
  if not os.path.exists(d):
    os.makedirs(d)

def ensureFile(file_pth):
  if not os.path.exists(file_pth):
    op = open(filename, "w")
    op.close()

class Create_file(object):
  def __init__(self, filename):
    if not os.path.exists(filename):
      op = open(filename, "w")
      op.close()

class Recorder(object):
    def __init__(self, filename):
        self.filename = filename
        Create_file(self.filename)
        self.content = ""

    def read(self):
        op = open(self.filename, "r")
        self.content = op.read()
        op.close()

    def write(self, new_content):
        op = open(self.filename, "w")
        op.write(new_content)
        op.close()

    def clear(self):
        op = open(self.filename, "w")
        op.close()
