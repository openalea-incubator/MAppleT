import openalea.stocatree.fruit as fruit
f = fruit.AppleFruit()
mass = []
for t in range(1,147):
    f.age = t
    mass.append(f.compute_mass())

import pylab
import numpy
age = range(1,147)
mass = numpy.array(mass)
pylab.plot(age, mass*1000)
pylab.xlabel('Times(days)')
pylab.ylabel('Fruit mass(grams)')
pylab.grid()

