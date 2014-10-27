import numpy
import time
from multiprocessing import Process, Manager, Lock



def func():
    a = numpy.random.rand(1500000)
    b = numpy.random.rand(1500000)

    nodata = 0.3

    start_time = time.clock()
    d = dict()
    for i in numpy.where((a > 0.0) & (a < 0.9) & (a != nodata)):
        for j in numpy.where((b > 0.0) & (b < 0.6) & (b != nodata)):
            #print len(numpy.intersect1d(i, j))
            for index in numpy.intersect1d(i, j):
                a_value = a[index]
                b_value = b[index]
                # if round(a_value, 5) in d:
                #     d[round(a_value, 5)] += 1
                # else:
                #     d[round(a_value, 5)] = 1
                try:
                    d[round(a_value, 6)]["freq"] += 1
                except:
                    d[round(a_value, 6)] = {
                        "data": [a_value, b_value],
                        "freq": 1
                    }

    print time.clock() - start_time, "seconds"
    print len(d)
    # for v in d.values():
    #       print v


def func_thread():
    a = numpy.random.rand(1000000)
    b = numpy.random.rand(1000000)

    nodata = 0.3

    print "here"
    manager = Manager()
    lock = Lock()
    d = manager.dict()
    ps = []
    start_time = time.clock()
    for i in numpy.where((a > 0.7) & (a < 0.9) & (a != nodata)):
        for j in numpy.where((b > 0.5) & (b < 0.9) & (b != nodata)):

            index = numpy.intersect1d(i, j)
            length = len(index)/2
            array1 = index[:length]
            array2 = index[length:]
            for processes in range(2):
                p = Process(target=f_thread, args=(d, a, b, array1, lock))
                ps.append(p)
                p.start()

            for p in ps:
                p.join()

    print time.clock() - start_time, "seconds"
    print len(d)

def f_thread(d, a, b, array_index, lock):
    for index in array_index:
        a_value = a[index]
        b_value = b[index]
        # if round(a_value, 5) in d:
        #     d[round(a_value, 5)] += 1
        # else:
        #     d[round(a_value, 5)] = 1

        with lock:
            try:

                d[round(a_value, 2)]["freq"] += 1
            except:
                d[round(a_value, 2)] = {
                    "data": [a_value, b_value],
                    "freq": 1
                }

func()