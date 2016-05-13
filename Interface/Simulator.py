from Impl.SimulatorImpl import SimulatorImpl 

class Simulator(object):

    """Docstring for Simulator. """

    def __init__(self, geoDataPath):
        self._impl = SimulatorImpl(geoDataPath)
    

    def createNewCase(self, caseName, numNode=100, centralNodeID=-1):
        """TODO: Docstring for createNew.
        :returns: TODO

        """

        self._impl.createNewCase(caseName, numNode, centralNodeID)

    def loadCase(self, caseName):
        """TODO: Docstring for loadCase.

        :caseName: TODO
        :returns: TODO

        """
        self._impl.loadCase(caseName)

    def simRandom(self, nth, maxConn, roots):
        """TODO: Docstring for simRandom.
        :returns: TODO

        """
        return self._impl.simRandom(nth, maxConn, roots)

    def simTwoPhase(self, nth, maxConn, roots):
        """TODO: Docstring for simTwoPhase.
        :returns: TODO

        """
        res = self._impl.simTwoPhasePrimary(nth, maxConn, roots)
        self._impl.simTwoPhaseBackup(nth, maxConn)
        return res

    def stub(self):
        """TODO: Docstring for stub.
        :returns: TODO

        """
        print 2

        
