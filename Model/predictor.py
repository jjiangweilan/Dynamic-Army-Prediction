import numpy as np 
import math
import json
from collections import defaultdict
PATH = '/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data.json'
STOP_UNITS = set([
    'ZERG_LOCUSTMP','ZERG_LARVA','ZERG_CHANGELING','ZERG_DRONE','ZERG_OVERLORD','ZERG_CREEPTUMOR','ZERG_CREEPTUMORQUEEN',
    'PROTOSS_ORACLESTASISTRAP','PROTOSS_PROBE',
    'TERRAN_POINTDEFENSEDRONE','TERRAN_SCV','TERRAN_MULE'])   
class Frame:
    def __init__(self,unit,time):
        self.unit = unit
        self.time = time

class Predictor:
    def __init__(self):
        with open(PATH) as f:
            self.json_data = json.load(f) #TO_DO: data to plot

        #self.data[race][obsUnit][comparedUnit]
        self.data = {'protoss': defaultdict(lambda:defaultdict(lambda : [])), 'zerg' : defaultdict(lambda:defaultdict(lambda : [])), 'terran': defaultdict(lambda:defaultdict(lambda : []))}
        #self.unitBuiltTime[race][unit]
        self.unitBuiltTime = {'protoss':defaultdict(lambda:[]),'zerg':defaultdict(lambda:[]),'terran':defaultdict(lambda:[])}
        self.unitBuiltTimeDensity = {'protoss':defaultdict(lambda:[]),'zerg':defaultdict(lambda:[]),'terran':defaultdict(lambda:[])}
        self._process()
        self._makeDensity(2600)

    def predict(self, race,obsUnit, time):
        timeFrame = int(time / 2600)
        unitVar = defaultdict(lambda:[])
        unitVarAvg = {}

        # get all corresponding unit variances 
        for n in obsUnit:
            for k,v in self.getVar(race,n):
                unitVar[k].append(v)
        
        # get the avg of the variance 
        for unit in unitVar:
            unitVarAvg[unit] = sum(unitVar[unit])/(len(unitVar[unit]))

        # weight the variance with built time density
        normalizedBTD = self._getNormalizedBTD()
        for k in unitVarAvg:
            if timeFrame < len(normalizedBTD[race][k]):
                unitVarAvg[k] *=  pow(math.e, -normalizedBTD[race][k][timeFrame])
            else:
                unitVarAvg[k] *= math.e

        rlt = [(k,unitVarAvg[k]) for k in unitVarAvg]
        predict = sorted(rlt,key=lambda x : x[1])
        for k,v in predict:
            print(k,v)

    def _getNormalizedBTD(self):
        normalized = defaultdict(lambda:{})
        for race in self.unitBuiltTimeDensity:
            for unit in self.unitBuiltTimeDensity[race]:
                temp = np.array(self.unitBuiltTimeDensity[race][unit])
                normalized[race][unit] = (temp-min(temp))/(max(temp)-min(temp))
        
        return normalized
        
    def _makeDensity(self, timeFrame):
        for r in self.unitBuiltTime:
            for unit in self.unitBuiltTime[r]:
                sort = sorted(self.unitBuiltTime[r][unit])

                last = 0
                tf = timeFrame
                for i,x in enumerate(sort):
                    if x > tf:
                        self.unitBuiltTimeDensity[r][unit].append(float(i-last) / len(sort))
                        last = i
                        tf += timeFrame
    def _process(self):
        for game in self.json_data:
            race = list(game.keys())[0].split('_')[0].lower()
            currGame = self._makeCurrentGame(game)
            self._fit(race, currGame)

            #make unitBuiltTime
            for k in game:
                self.unitBuiltTime[race][k] += game[k]
    
    def _fit(self, race, currGame):
        for i in range(len(currGame)):
            if i == len(currGame) - 1:break
            observed = set()
            for ii in range(i,len(currGame)):
                if currGame[ii].unit not in observed and currGame[ii].unit != currGame[i].unit:
                    observed.add(currGame[ii].unit)
                    self.data[race][currGame[i].unit][currGame[ii].unit].append(currGame[ii].time - currGame[i].time) #currently record the first one, try second one

    def _makeCurrentGame(self,game):
        #return a 1d array that's sorted by Frame.time   
        currGame = []
        for unit,times in game.items(): 
            u = [Frame(unit, t) for t in times if unit not in STOP_UNITS and 'ZERG_CHANGEL' not in unit]
            currGame += u
        currGame = sorted(currGame, key=lambda x:x.time)
        
        return currGame

    def getVar(self, race, unit):
        unit = race.upper() + '_' + unit.upper()
        array = []
        var = []
        # calculate the variance of each units
        for _,k in enumerate(p.data[race][unit]):
            units = p.data[race][unit][k]
            array.append([k,math.sqrt(np.var(units))])

        # sort the variance
        for k,v in sorted(array, key=lambda x:x[1]):
            if v == 0: v = math.inf
            var.append((k,v))

        return var

p = Predictor()

#graph
import matplotlib.pyplot as plt

#observe variance
def obsVar(race, unit):
    #print multiple figs which have 3 rows' axis

    unit = race.upper() + '_' + unit.upper()
    last=0
    count = 0
    count_f = 3
    fig, ax = plt.subplots(nrows=3)
    for row,k in enumerate(p.data[race][unit],last):
        count +=1
        if count > count_f:
            last = count
            count_f += 3
            fig, ax = plt.subplots(nrows=3)
        ax[row-last].plot(p.data[race][unit][k],range(len(p.data[race][unit][k])),'ro',marker="o",markersize=0.7,label=k)
        ax[row-last].legend(loc='best')
    plt.tight_layout()
    plt.show()
    plt.cla()


    

def obsBuiltTime(race,unit): 
    unit = race.upper() + '_' + unit.upper()
    fig, ax = plt.subplots(nrows=2)
    ax[0].plot(p.unitBuiltTime[race][unit], range(len(p.unitBuiltTime[race][unit])),'ro',marker="o",markersize=0.7)
    print(p.unitBuiltTimeDensity[race][unit])
    ax[1].plot(range(len(p.unitBuiltTimeDensity[race][unit])),p.unitBuiltTimeDensity[race][unit])
    ax[0].set_xlim(0)
    ax[1].set_ylim((0,1))
    plt.show()
RACE='protoss'
UNIT='HIGHTEMPLAR'


p.predict('protoss',['ZEALOT','ROBOTICSFACILITY','STALKER','FORGE'],18000)





