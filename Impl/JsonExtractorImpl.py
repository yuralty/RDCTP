import json
import re
import numpy


class JsonExtractorImpl(object):

    """Docstring for ExtractorImpl. """

    def __init__(self):
        """TODO: to be defined1. """
        
    def extract(self, inFile, out):
        """TODO: Docstring for extract.

        :arg1: TODO
        :returns: TODO

        """

        def polyMean(polyInfo):
            """TODO: Docstring for polyMean.

            :polyInfo: with format 'MULTIPOLYGON ((($longitude $latitude, ...)))'
            :returns: mean longitude and latitude of polygon

            """
            geoInfo = re.search('\(\(\(.*\)\)\)', polyInfo).group(0).lstrip('(').rstrip(')')
            lgts = []
            ltts = []
            for loc in geoInfo.split(','):
                lgts.append(float(loc.split()[0]))
                ltts.append(float(loc.split()[1]))
            return numpy.mean(lgts), numpy.mean(ltts)
            

        data = json.loads(inFile.read())
        # structure of data: {'type', 'features': list of poles}
        
        with open(out, 'w') as outFile:

            for pole in data['features']:
                geo = pole['geometry']['coordinates']
                assert(len(geo) == 2)
                outFile.write("%s %s\n" % (geo[0], geo[1]))

