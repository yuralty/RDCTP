import numpy as np
import os, sys
import random
import math

class SimulatorImpl(object):

    """Docstring for SimulatorImpl. """

    def __init__(self, geoDataPath):
        """TODO: to be defined1. """
        self.data = np.loadtxt(geoDataPath)
        self.testRoot = 'tests/'

    def createNewCase(self, caseName, numNode, centralNodeID):
        """TODO: Docstring for createNewCase.
        :returns: TODO

        """
        caseName = self.testRoot + caseName
        if os.path.exists(caseName):
            print "case %s exists" % caseName
            return

        print "create case: %s" % caseName
        if centralNodeID == -1:
            centralNodeID = random.randint(0, len(self.data)-1)
            lon, lat = self.data[centralNodeID][0], self.data[centralNodeID][1]

        dist = []
        for i in xrange(len(self.data)):
            node = self.data[i]
            dist.append(((node[0]-lon)**2 + (node[1]-lat)**2, i))

        dist.sort(key=lambda tup: tup[0])  # sorts in place       

        os.makedirs(caseName)
        out = caseName + "/topology.dat"
        with open(out, 'w') as outFile:
            for i in xrange(numNode):
                (lon, lat) = self.data[dist[i][1]]
                outFile.write('%f %f\n' % (lon, lat))

    def loadCase(self, caseName):
        self.dataPath = self.testRoot + caseName
        topoDataPath = self.dataPath + '/topology.dat'
        self.data = np.loadtxt(topoDataPath)

    def loadPrimary(self, primaryName):
        """TODO: Docstring for loadPrimary.
        :returns: TODO

        """
        from ast import literal_eval
        primaryPath = self.dataPath + '/' + primaryName
        with open(primaryPath, 'r') as inFile:
            self.roots = literal_eval(inFile.readline())
            self.parents = literal_eval(inFile.readline())
        
    def computeNeighbor(self, n, maxConn):
        """TODO: Docstring for computeNeighbor.
        :returns: TODO

        """
        dist = np.zeros((n, n))
        neighbors = np.zeros((n, maxConn))
        for i in xrange(n):
            for j in xrange(n):
                if i == j:
                    dist[i][j] = 0
                else:
                    dist[i][j] =\
                        math.sqrt((self.data[i][0]-self.data[j][0])**2 +\
                        (self.data[i][1]-self.data[j][1])**2)

        for i in xrange(n):
            distToI = []
            for j in xrange(n):
                distToI.append((dist[i][j], j))
            distToI.sort(key=lambda tup: tup[0])
            for j in xrange(1, maxConn+1):
                neighbors[i][j-1] = distToI[j][1]
        
        return dist, neighbors

    def simTwoPhasePrimary(self, nth, maxConn, roots=None):
        """TODO: Docstring for simTwoPhase.
        :returns: TODO

        """

        out= self.dataPath + '/twoPhasePrimary_%d.dat' % nth
        n = len(self.data)

        # parameters
        #nth = 20
        #maxConn = 10
        #m = int(n/nth * math.log(n))

        if roots is None:
            roots = []
            ids = range(n)
            random.shuffle(ids)
            roots = ids[ : int(n/nth*math.log(n))]
            roots.sort()

        m = len(roots)

        dist, neighbors = self.computeNeighbor(n, maxConn)

        parents = [-1] * n
        delays = [0] * n
        rootInfo = {}
        for root in roots:
            parents[root] = root
            rootInfo[root] = {'num': 1, 'delay': 0}

        for i in xrange(n-m):
            minDelayInc = sys.maxint
            MDId = -1
            parentId = -1
            rootId = -1
            sequence = range(n)
            random.shuffle(sequence)
            for nid in sequence:
                if parents[nid] != -1: continue
                if minDelayInc == 0: break

                delay = sys.maxint
                if nid in roots:
                    continue
                for nb in neighbors[nid]:
                    nb = int(nb)
                    if parents[nb] == -1: continue
                    root = nb
                    while parents[root] != root: root = parents[root]
                    if rootInfo[root]['num'] >= nth: continue

                    if dist[nid][nb] + delays[nb] <= rootInfo[root]['delay']:
                        minDelayInc = 0
                        MDId = nid
                        parentId = nb
                        rootId = root
                        break
                    elif dist[nid][nb] + delays[nb] - rootInfo[root]['delay'] <\
                        minDelayInc:
                        minDelayInc = dist[nid][nb] + delays[nb] -\
                        rootInfo[root]['delay']
                        MDId = nid
                        parentId = nb
                        rootId = root

            try:
                assert(MDId != -1)
            except:
                print "restart twophase"
                return self.simTwoPhasePrimary(nth, maxConn)
            #print MDId, parentId, minDelayInc, root
            parents[MDId] = parentId
            delays[MDId] = delays[parents[parentId]] + dist[MDId][parentId]
            rootInfo[rootId]['delay'] += minDelayInc
            rootInfo[rootId]['num'] += 1

        #print roots
        #print parents

        with open(out, 'w') as outFile:
            outFile.write("%s\n" % str(roots))
            outFile.write("%s\n" % str(parents))
        
        s = 0
        for r, stats in rootInfo.iteritems():
            s += stats['delay']
        print s
        return s

    def simTwoPhaseBackup(self, nth, maxConn):

        out= self.dataPath + '/twoPhaseBackup_%d.dat' % nth
        self.loadPrimary('twoPhasePrimary.dat')
        dist, neighbors = self.computeNeighbor(len(self.data), maxConn)

        class Node(object):
        
            """Docstring for Node. """
        
            def __init__(self, mdid=-1):
                self.mdid = mdid
                self.parent = None
                self.backup = None
                self.children = []
                self.delay = 0
                self.size = 1

            def dfs(self, dist):
                """TODO: Docstring for dfs.
                :returns: TODO

                """
                if len(self.children) == 0: return self.delay, self.size
                max_delay = 0
                for ch in self.children:
                    ch_delay, ch_size = ch.dfs(dist)
                    self.size += ch_size
                    if ch_delay + dist[self.mdid][ch.mdid] > max_delay:
                        max_delay = ch_delay + dist[self.mdid][ch.mdid]
                self.delay = max_delay
                return self.delay, self.size

        tree = []
        for i in xrange(len(self.parents)):
            tree.append(Node(i))
        
        for ch in xrange(len(self.parents)):
            p = self.parents[ch]
            if p == ch: continue
            tree[ch].parent = tree[p]
            tree[p].children.append(tree[ch])

        #for ch in xrange(20):
            #if tree[ch].parent != None:
                #print tree[ch].parent.mdid
            #print [cch.mdid for cch in tree[ch].children]
        for root in self.roots:
            tree[root].dfs(dist)

        n = len(self.data)
        m = len(self.roots)
        backups = [-1] * n
        for i in xrange(n-m):
            minDelayInc = sys.maxint
            MDId = -1
            backupId = -1
            rootId = -1
            sequence = range(n)
            random.shuffle(sequence)
            for nid in sequence:
                if backups[nid] != -1: continue
                if nid in self.roots: continue

                root = self.parents[nid]
                while root != self.parents[root]: root = self.parents[root]

                for nb in neighbors[nid]:
                    nb = int(nb)
                    newRoot = self.parents[nb]
                    while newRoot != self.parents[newRoot]: newRoot =\
                        self.parents[newRoot]
                    if root == newRoot: continue

                    #if tree[newRoot].size >= nth: continue


                    if minDelayInc > dist[nid][nb] + tree[nid].delay -\
                            tree[nb].delay:
                        minDelayInc = dist[nid][nb] + tree[nid].delay -\
                            tree[nb].delay
                        MDId = nid
                        backupId = nb
                        rootId = newRoot

                    elif minDelayInc == dist[nid][nb] + tree[nid].delay -\
                            tree[nb].delay and tree[newRoot].size <\
                            tree[rootId].size:
                        minDelayInc = dist[nid][nb] + tree[nid].delay -\
                            tree[nb].delay
                        MDId = nid
                        backupId = nb
                        rootId = newRoot

            try:
                assert(MDId != -1)
            except: #choosing a random neighbor as backup parent
                flag = False
                for nid in xrange(n):
                    if backups[nid] != -1 or nid in self.roots: continue
                    nbs = neighbors[nid]
                    random.shuffle(nbs)
                    root = self.parents[nid]
                    while root != self.parents[root]: root = self.parents[root]
                    for nb in nbs:
                        nb = int(nb)
                        if nb == self.parents[nid]: continue
                        newRoot = self.parents[nb]
                        #while newRoot != self.parents[newRoot]: newRoot =\
                            #self.parents[newRoot]
                        #if tree[newRoot].size < nth:
                        MDId = nid
                        rootId = newRoot
                        backupId = nb
                        flag = True
                        break
            #print MDId, parentId, minDelayInc, root
            backups[MDId] = backupId
            tree[rootId].size += 1

        with open(out, 'w') as outFile:
            outFile.write("%s\n" % str(self.roots))
            outFile.write("%s\n" % str(backups))

                

    def simRandom(self, nth, maxConn, roots=None):
        """TODO: Docstring for simTwoPhase.
        :returns: TODO

        """

        out = self.dataPath + '/randomPrimary.dat'
        n = len(self.data)

        # parameters
        #nth = 20
        #maxConn = 10
        #m = int(n/nth * math.log(n))

        if roots is None:
            roots = []
            ids = range(n)
            random.shuffle(ids)
            roots = ids[ : int(n/nth*math.log(n))]
            roots.sort()

        m = len(roots)
        dist = np.zeros((n, n))
        neighbors = np.zeros((n, maxConn))
        for i in xrange(n):
            for j in xrange(n):
                if i == j:
                    dist[i][j] = 0
                else:
                    dist[i][j] =\
                        math.sqrt((self.data[i][0]-self.data[j][0])**2 +\
                        (self.data[i][1]-self.data[j][1])**2)

        for i in xrange(n):
            distToI = []
            for j in xrange(n):
                distToI.append((dist[i][j], j))
            distToI.sort(key=lambda tup: tup[0])
            for j in xrange(1, maxConn+1):
                neighbors[i][j-1] = distToI[j][1]


        parents = [-1] * n
        delays = [0] * n
        rootInfo = {}
        for root in roots:
            parents[root] = root
            rootInfo[root] = {'num': 1, 'delay': 0}

        cnt = 0
        lastCnt = -1
        rounds = 0
        while cnt < n-m:
            if lastCnt != cnt:
                rounds = 0
            else:
                rounds += 1
            if rounds > 50000:
                print "restart random"
                return self.simRandom(nth, maxConn)
            lastCnt = cnt
            parentId = random.randint(0, n-1)
            while parents[parentId] == -1: 
                parentId = random.randint(0, n-1)
            
            nbs = []
            for nb in neighbors[parentId]:
                nb = int(nb)
                if parents[nb] == -1:
                    nbs.append(nb)
            if len(nbs) == 0:
                continue

            root = parentId
            while parents[root] != root:
                root = parents[root]
            if rootInfo[root]['num'] >= nth:
                continue

            randNb = nbs[random.randint(0, len(nbs)-1)]
            parents[randNb] = parentId
            delays[randNb] = delays[parentId] + dist[randNb][parentId]
            rootInfo[root]['num'] += 1
            if rootInfo[root]['delay'] < delays[randNb]:
                rootInfo[root]['delay'] = delays[randNb]

            cnt += 1

        with open(out, 'w') as outFile:
            outFile.write("%s\n" % str(roots))
            outFile.write("%s\n" % parents)

        s = 0
        for r, stats in rootInfo.iteritems():
            s += stats['delay']
        print s
        return s


    def stub(self):
        """TODO: Docstring for stub.
        :returns: TODO

        """
