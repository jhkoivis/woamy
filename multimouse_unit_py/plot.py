
import numpy
import pylab

data = numpy.loadtxt('test_data.txt')

pylab.plot(data[:,0], data[:,1])
pylab.plot(data[:,0], data[:,2])
pylab.plot(data[:,0], data[:,3])

pylab.show()


