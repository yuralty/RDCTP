from Impl.PlotterImpl import PlotterImpl
import csv

class Plotter(object):

    """
    plot data
    """

    def __init__(self):
        """TODO: to be defined1.

        """
        self._impl = PlotterImpl()


    def plot(self):
        """TODO: Docstring for extract.

        :csvFile: TODO
        :out: TODO
        :returns: TODO

        """
        self._impl.plotPrimary()
        self._impl.plotDifferentNth()

