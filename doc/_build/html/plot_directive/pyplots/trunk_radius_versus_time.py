import numpy
import pylab

data = numpy.loadtxt('../data/trunk.dat', converters={0:lambda x:1})
pylab.clf();
pylab.plot(1994+data[:,1]/365, 100* data[:,2]);
pylab.xlabel('Time(days)'); 
pylab.ylabel('Trunk radius (cm)');
#pylab.savefig('trunk_radius_versus_time.png')

