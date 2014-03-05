import data
import pylab

pylab.clf()

fig = pylab.plot(data.years, data.lpy/data.mapplet, 'or-', data.years, data.lpy2/data.mapplet, 'x-')
pylab.legend(['lpy run/mapplet', 'lpy animate/mapplet'],loc='best')
pylab.xlabel('Simulated years')
pylab.ylabel('Ratio mapplet/lpy')


