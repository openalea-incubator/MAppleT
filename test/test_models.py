from openalea.plantik.tools import runlpy
from openalea.stocatree import get_shared_data
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication([])

def test():
    try:
        l = runlpy(get_shared_data('stocatree.lpy'))
    except:
        pass
