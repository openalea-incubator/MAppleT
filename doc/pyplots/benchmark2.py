import pylab
import data


pylab.clf()
fig = pylab.plot(data.years, data.mapplet, data.years, data.lpy, 'or-',data.years, data.lpy2,'x-' )
l = pylab.legend(['mapplet','lpy run','lpy animate'],loc='best')
pylab.xlabel('Simulated years'); 
pylab.ylabel('Simulation duration (s)') 


