import csv
import re
import numpy


class ExtractorImpl(object):

    """Docstring for ExtractorImpl. """

    def __init__(self):
        """TODO: to be defined1. """
        
    def extract(self, csvFile, out):
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
            

        reader = csv.reader(csvFile, delimiter=',')
        nodes = [] # (id, longitude, latitude) tuple
        for row in reader:
            try:
                if not row[1].startswith('MULTIPOLYGON'):
                    continue
                lgt, ltt = polyMean(row[1])
                #print int(row[0]), lgt, ltt
                #print lgt, ltt
                nodes.append([int(row[0]), lgt, ltt])

            except:
                pass

        with open(out, 'w') as fout:
            for line in nodes:
                for item in line:
                    fout.write("%s " % item)
                fout.write("\n")


