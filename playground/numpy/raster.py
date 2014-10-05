import numpy

print "here"
x = numpy.arange(20)


values = numpy.array([100,500, 700, 800, 100])
print values

mask = numpy.greater(values, 110)
print mask
masked = numpy.choose(mask, values)
print masked
print numpy.where(values > 110, values, 0)
#set the min = 100 and max = 800
print numpy.clip(values, 100, 800)

print "mortacci tua e chi non te lo dice con la mano alzata"