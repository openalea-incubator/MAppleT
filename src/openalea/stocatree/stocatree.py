import openalea.lpy as lpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from vplants.plantgl.all import Viewer
app = QApplication([])
Viewer.start()

def run():
    app = QApplication([])
    time1 = time.time()
    l = lpy.Lsystem('stocatree.lpy')
    iter_by_dt = 8.05
    nb_year = 2
    N = int(365*iter_by_dt * nb_year)

    #N = 3000 #-> end dec 1994
    #N = 4400 #-> end june 1995
    #N = 8000 #-> end sept 1996

    res = l.iterate(N)
    l.plot(res)
    #Viewer.frameGL.setBgColor(170,170,255)
    Viewer.frameGL.saveImage('output.png', 'png')

    time2 = time.time()
    print 'Simulation took %s' % str(time2-time1)
    l.plot(res)



if __name__=="__main__":
    import sys
    import lsprofcalltree
    import cProfile
    args = sys.argv

    if len(args)==1:
        run()
    elif len(args)==2 and args[1]=='--profile':
        p = cProfile.Profile()
        p.run('run()')
        k = lsprofcalltree.KCacheGrind(p)
        data = open('prof.kgrind', 'w+')
        k.output(data)
        data.close()


