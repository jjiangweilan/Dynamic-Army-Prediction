import matplotlib.pyplot as plt
import math
import json
import sys

PATH = '/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data.json'
class Grapher:
    "graph processed data \
    the graph is designed to better observe the \
    relation of one unit with all other units\
    "

    def __init__(self):
        with open(PATH) as f:
            self.data = json.load(f) #TO_DO: data to plot

        self.processData()
        #print data info
        print('protoss amount:{0}, terran amount:{1}, zerg amount:{2}'.format(len(self.data['protoss']),len(self.data['terran']),len(self.data['zerg'])))
    def processData(self):
        temp = {'protoss':[],'terran':[],'zerg':[]}
        for game in self.data:
            race =  list(game.keys())[0].split('_')[0]
            if race == 'TERRAN':
                temp['terran'].append(game)
            elif race == 'PROTOSS':
                temp['protoss'].append(game)
            elif race == 'ZERG':
                temp['zerg'].append(game)
            
        self.data = temp

    def plotInGame(self, race, index, unitToObserve):
        unitToObserve = self.toUpper(race, unitToObserve)
        totalUnits = len(self.data[race][index])
        max_time = self.getMax(self.data[race][index])

        #creat the sublot
        fig, ax = self.createGraph(totalUnits)

        obs_unit = self.data[race][index][unitToObserve] # the unit to be compared to all others
        keys = self.data[race][index].keys() #names of the units
        
        keyIter = iter(keys)
        shape = ax.shape
        count = 0
        for row in range(shape[0]):
            for col in range(shape[1]):
                try:
                    key = next(keyIter)
                    compare_unit = self.data[race][index][key]

                    ax[row,col].plot(obs_unit,range(len(obs_unit)))
                    ax[row,col].plot(compare_unit,range(len(compare_unit)))
                    ax[row,col].set_title(key.split('_')[1].lower(),loc='center')
                    ax[row,col].set_xlim(0,max_time + 500)
                    count += 1
                except StopIteration:
                    break
        
        fig.tight_layout()
        plt.show()
    
    def toUpper(self,race, name):
        return race.upper() + '_' + name.upper()

    def plotAmongGame(self, race, unitToObserve, unitToCompare, maxObs=None):
        maxObs = len(self.data[race]) if maxObs == -1 else maxObs - 1
        fig, ax = self.createGraph(maxObs)
        fig.canvas.set_window_title('{} vs {}'.format(unitToObserve, unitToCompare))

        unitToObserve = self.toUpper(race, unitToObserve)
        unitToCompare = self.toUpper(race, unitToCompare)
        

        shape = ax.shape
        count = 0
        for row in range(shape[0]):
            for col in range(shape[1]):
                try:
                    if count >= maxObs: break
                    obs_unit = self.data[race][count][unitToObserve]
                    compare_unit = self.data[race][count][unitToCompare]

                    #max_time
                    max_time = 0
                    for n in obs_unit + compare_unit:
                        if n > max_time: max_time = n

                    ax[row,col].plot(obs_unit,range(len(obs_unit)))
                    ax[row,col].plot(compare_unit,range(len(compare_unit)))
                    
                    ax[row,col].set_xlim(0,max_time + 500)
                    count += 1
                except StopIteration:
                    break
                except KeyError:
                    count += 1
                    continue
            
        
        fig.tight_layout()
        
        plt.show()

    def createGraph(self,rows):
        COLS = 5
        rows = math.ceil(rows/float(COLS))
        if rows == 1:rows = 2
        return plt.subplots(nrows=rows, ncols=COLS)

        
    def getMax(self,data):
        max_ = 0
        for k in data:
            for n in data[k]:
                if n > max_:
                    max_ = n
        return max_

g = Grapher()

while(True):
    option = input('InGame(i) or AmongGame(a): ')
    if option == 'InGame' or option == 'i':
        options = input('race, unitToObserve (seperate by a space)\n').split(' ')
        g.plotInGame(options[0],int(options[1]),options[2])
    elif option == 'AmongGame' or option == 'a':
        options = input('race, unitToObserve, unitToCompare, maxObs(-1 for maximum) (seperate by a space)\n').split(' ')
        g.plotAmongGame(options[0], options[1],options[2], int(options[3]))
    else:
        print('wrong input')