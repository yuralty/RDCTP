from Interface import Extractor, Simulator
import sys, os
import numpy
import matplotlib.pyplot as plt
import math, random

def extract():
    """TODO: Docstring for extract.
    :returns: TODO

    """
    DATAPATH="data/Utility_Poles.geojson"
    ext = Extractor.Extractor()
    with open(DATAPATH, 'r') as inFile:
        ext.extract(inFile, 'out')

def truncate(maxNode, numSample):
    """TODO: Docstring for truncate.

    :maxNode: TODO
    :numSample: TODO
    :returns: TODO

    """


def plotMap(fpath):
    """ Plot map from a data file

    :x: TODO
    :y: TODO
    :returns: TODO

    """
    data = numpy.loadtxt(fpath)

    x = data[:, 0]
    y = data[:, 1]
    plt.plot(x, y, 'o')
    plt.show()


if __name__ == "__main__":
    GEODATAPATH = 'data/topology.dat'
    sim = Simulator.Simulator(GEODATAPATH)
    #for i in xrange(1, 31):
        #for j in xrange (1, 11):
            #sim.createNewCase('random_%d_%d' % (i*100, j), i*100)

    n = 1000
    nth = 80
    maxConn = 10
    for i in xrange(5, 15):
        n = 100*i
        with open('tests/res/res_%d_%d.dat' % (nth, n), 'w') as res:
            m = int(n/nth * math.log(n))
            roots = []
            ids = range(n)

            res.write('%d\t%d\t%d\n' % (nth, maxConn, m))
            for j in xrange(1, 11):
                print 'running case: %d-%d' % (n, j)
                sim.loadCase('random_%d_%d' % (n, j))

                random.shuffle(ids)
                roots = ids[ : m]
                roots.sort()

                s1 = sim.simTwoPhase(nth, maxConn, roots)
                s2 = sim.simRandom(nth, maxConn, roots)
                res.write('%f\t%f\n' % (s1, s2))
            



