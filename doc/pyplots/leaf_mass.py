import pylab
import openalea.stocatree.leaf as leaf
import numpy

l = leaf.AppleLeaf()
days = numpy.arange(0,12, 0.1)

m = []
for d in days:
    l.age = d
    # 16 so that number is greater than preformed leaves maximum value of 8.
    s = l.compute_area(16)
    m.append(l.compute_mass())

pylab.plot(days, m, '-')
pylab.xlabel('Time (days)')
pylab.ylabel('Mass g')
pylab.grid(True)
pylab.title('Mass of a leaf')
