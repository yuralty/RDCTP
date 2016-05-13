import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class PlotterImpl(object):

    """Docstring for PlotterImpl. """

    def __init__(self):
        """TODO: to be defined1. """

    def plotPrimary(self):
        """TODO: Docstring for plotPrimary.
        :returns: TODO

        """

        fig, ax = plt.subplots()
        ax.grid(True)
        ax.set_xlim([400, 1500])

        NORM = 1

        ns = []
        ys1 = []
        ys2 = []
        errs1 = []
        errs2 = []
        rootPath = 'tests/res/'
        for i in xrange(5, 15):
            x = i*100
            ns.append(x)
            fname = 'res_20_%d.dat' % x
            data = np.loadtxt(rootPath+fname, skiprows=1)
            ys1.append(np.mean(data[:,0])*NORM)
            errs1.append(np.std(data[:,0])*NORM)
            ys2.append(np.mean(data[:,1])*NORM)
            errs2.append(np.std(data[:,1])*NORM)

        s = 0
        for i in xrange(10):
            s += ys1[i]/ys2[i]
        s/=10
        print 1 - s


        rand = ax.errorbar(ns, ys2, yerr=errs2, fmt='--^')
        heu = ax.errorbar(ns, ys1, yerr=errs1, fmt='-o')
        ax.legend([rand, heu], ["Random", "Two-step Greedy"], loc=2)
        ax.set_xlabel("Number of MDs")
        ax.set_ylabel("Normalized Data Collection Time")

        plt.show()
        plt.savefig('non-fail.png')

    def plotDifferentNth(self):
        """TODO: Docstring for plotPrimary.
        :returns: TODO

        """

        fig, ax = plt.subplots()
        ax.grid(True)
        ax.set_xlim([400, 1500])

        NORM = 1

        ns = []
        ys1 = []
        ys2 = []
        ys3 = []
        errs1 = []
        errs2 = []
        errs3 = []
        rootPath = 'tests/res/'
        for i in xrange(5, 15):
            x = i*100
            ns.append(x)
            fname = 'res_20_%d.dat' % x
            data = np.loadtxt(rootPath+fname, skiprows=1)
            ys1.append(np.mean(data[:,0])*NORM)
            errs1.append(np.std(data[:,0])*NORM)
            fname = 'res_40_%d.dat' % x
            data = np.loadtxt(rootPath+fname, skiprows=1)
            ys2.append(np.mean(data[:,0])*NORM)
            errs2.append(np.std(data[:,0])*NORM)
            fname = 'res_80_%d.dat' % x
            data = np.loadtxt(rootPath+fname, skiprows=1)
            ys3.append(np.mean(data[:,0])*NORM)
            errs3.append(np.std(data[:,0])*NORM)


        heu20 = ax.errorbar(ns, ys1, yerr=errs1, fmt='-o')
        heu40 = ax.errorbar(ns, ys2, yerr=errs2, fmt='-*')
        heu80 = ax.errorbar(ns, ys3, yerr=errs3, fmt='-^')
        ax.legend([heu20, heu40, heu80], ["Nth = 20", "Nth = 40", "Nth = 80"], loc=2)
        ax.set_xlabel("Number of MDs")
        ax.set_ylabel("Normalized Data Collection Time")

        plt.savefig('diffnth.png')
            

        
