import json
import bisect
import copy
import math

# Usage:
#
# import jsonimporter
# somevar = jsonimporter.fullgame(filename, tilesize)
#
# this will return a fullgame() object with all of the timetiles
# The filename should be formatted 'dummygame.json' if it's in the same directory
#
# To view the timetiles, use:
# somevar.printTiles()
# Timetiles contain timestamps of all units which were built during its duration
#
# To return a list of sums:
# sums = somevar.sumTiles(True) The parameter decides whether to print or not
# the return value can then be indexed by sums[player][tileindex]

class timetile:
    _playerdict = dict()
    _tilesum = dict()

    # tile index would be the index of the timetile
    def __init__(self, tileindex):
        self._tindex = tileindex

    def setUnitdict(self,dict):
        self._playerdict = dict

    def getUnitdict(self):
        return self._playerdict

    def getTileind(self):
        return self._tindex

    def computeTilesum(self):
        for unit,count in self._playerdict.items():
            self._tilesum[unit] = len(count)
        return self._tilesum

class fullgame:
    _p1t = []
    _p2t = []
    _tilesize = 0

    def __init__(self, filename, tilesize):
        self._tilesize = tilesize
        self.importjson(filename)

    def importjson(self, filename):
        with open(filename) as file:
            idata = json.load(file)

        # set the dictionaries for each player
        p1 = idata["p1"]["units"]
        p2 = idata["p2"]["units"]

        # create a sequence of all the timestamps
        p1times = p1.values()
        p2times = p2.values()

        # find the max timestamp (the last unit created)
        alltimes = p1times + p2times
        timestamps = []
        for time in alltimes:
            timestamps = timestamps + time

        maxt = max(timestamps)

        # create the class objects
        # number of 8-minute time tiles in the game
        gametiles = int(math.ceil(maxt/float(self._tilesize)))
        for i in range(0, gametiles):
            self._p1t = self._p1t + [timetile(i)]
            self._p2t = self._p2t + [timetile(i)]

        # Iterate through the time tiles for the game
        for tile in range(0, gametiles):
            # The abridged dictionary for this time tile
            abrdict = dict()
            for unit,counts in p1.items():
                # Get the indices for the time cutoff of this tile
                tileindu = bisect.bisect_left(counts,(tile+1)*self._tilesize)
                tileindl = bisect.bisect_left(counts,(tile)*self._tilesize)
                # Abridge the dictionary to the tile
                abrdict[unit] = counts[tileindl:tileindu]

            # Set the abriged list for this tile
            self.setPonedict(tile,copy.deepcopy(abrdict))

            # Do the above for player 2
            for unit,counts in p2.items():
                tileindu = bisect.bisect_left(counts,(tile+1)*self._tilesize)
                tileindl = bisect.bisect_left(counts,(tile)*self._tilesize)
                abrdict[unit] = counts[tileindl:tileindu]

            self.setPtwodict(tile,copy.deepcopy(abrdict))

        # Returns a fullgame object with p1t and p2t as lists of the timetiles
        # For instance, fgame.p1t[0] is the units for player 1 between 0 and 480

    def setPlayerone(self, tilelist):
        self._p1t = tilelist

    def setPlayertwo(self, tilelist):
        self._p2t = tilelist

    def setPonedict(self, index, dict):
        self._p1t[index].setUnitdict(dict)

    def setPtwodict(self, index, dict):
        self._p2t[index].setUnitdict(dict)

    def getPlayerone(self):
        return self._p1t

    def getPlayertwo(self):
        return self._p2t

    def getTilesize(self):
        return self._tilesize

    # Computes the sum of the tiles and prints it
    # Returns a list of all the dictionaries for the tile sums
    # The total list can be indexed by totallist[player][tile]
    # For the sum of an individual tile, use computeTilesum() on the tile
    def sumTiles(self, doprint):
        p1 = self.getPlayerone()
        p2 = self.getPlayertwo()
        tsize = self.getTilesize()

        unittotals = dict.fromkeys(p1[0].getUnitdict(),0)
        totalpone = []
        totalptwo = []
        sumlist = [totalpone, totalptwo]

        if doprint:
            print("Player 1:")

        for tile in p1:
            index = tile.getTileind()
            tsum = tile.computeTilesum()
            for unit in tsum:
                unittotals[unit] = unittotals[unit] + tsum[unit]
            if doprint:
                print("Tile: " + str(index) + ", t = " + str(index*tsize) + " to " + str((index+1)*tsize-1))
                print(unittotals)
            totalpone.append(copy.deepcopy(unittotals))

        if doprint:
            print("Player 2:")

        unittotals = dict.fromkeys(p2[0].getUnitdict(),0)
        for tile in p2:
            index = tile.getTileind()
            tsum = tile.computeTilesum()
            for unit in tsum:
                unittotals[unit] = unittotals[unit] + tsum[unit]
            if doprint:
                print("Tile: " + str(index) + ", t = " + str(index*tsize) + " to " + str((index+1)*tsize-1))
                print(unittotals)
            totalptwo.append(copy.deepcopy(unittotals))

        return sumlist

    # Prints tiles and their times in a readable format
    # fgame input is a fullgame() object
    # To get the dictionaries for each timetile, use:
    # fgame.getPlayerone()[tileIndex].getUnitdict()
    def printTiles(self):
        tsize = self.getTilesize()
        print("Player 1:")
        for tile in self.getPlayerone():
            index = tile.getTileind()
            print("Tile: " + str(index) + ", t = " + str(index*tsize) + " to " + str((index+1)*tsize-1))
            print(tile.getUnitdict())
        print("Player 2:")
        for tile in self.getPlayertwo():
            index = tile.getTileind()
            print("Tile: " + str(index) + ", t = " + str(index*tsize) + " to " + str((index+1)*tsize-1))
            print(tile.getUnitdict())
