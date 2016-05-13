from Impl.JsonExtractorImpl import JsonExtractorImpl
import csv

class Extractor(object):

    """
    Extract location of building from Utility_Poles.geojson
    Truncate extracted data to a small dataset
    """

    def __init__(self):
        """TODO: to be defined1.

        """
        self._impl = JsonExtractorImpl()


    def extract(self, inFile, out):
        """TODO: Docstring for extract.

        :csvFile: TODO
        :out: TODO
        :returns: TODO

        """
        self._impl.extract(inFile, out)

    def truncate(self, csvFile, maxNodes, out):
        """TODO: Docstring for truncate.

        :csvFile: TODO
        :maxNodes: TODO
        :out: TODO
        :returns: TODO

        """
        self._impl.truncate(csvFile, maxNodes, out)


        
