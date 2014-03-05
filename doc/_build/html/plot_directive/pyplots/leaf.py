import pylab
import openalea.stocatree.leaf as leaf
import numpy

l = leaf.AppleLeaf()
days = numpy.arange(0,12, 0.1)

s = []
for d in days:
    l.age = d
    # 16 so that number is greater than preformed leaves maximum value of 8.
    s.append(l.compute_area(16))

pylab.plot(days, s, '-')
pylab.xlabel('Time (days)')
pylab.ylabel('Surface **(cm^2)**')
pylab.grid(True)
pylab.title('Surface area of a leaf')
