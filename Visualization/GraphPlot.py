import matplotlib.pyplot as plt
import math
import json

class Grapher:
    "graph processed data \
    the graph is designed to better observe the \
    relation of one unit with all other units\
    "

    def __init__(self,unitToObserve):
        with open('/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data.json') as f:
            self.data = json.load(f) #TO_DO: data to plot
            self.data = self.data[0] #get the match dictionary from the array
        self.unitToObserve = unitToObserve
        self.totalUnits = len(self.data)
        self.max_time = self.getMax(self.data)

        #creat the sublot
        COLS = 5
        rows = math.ceil(self.totalUnits/float(COLS))
        if rows == 1:rows = 2
        self.fig, self.ax = plt.subplots(nrows=rows, ncols=COLS)
    def plot(self):
        obs_unit = self.data[self.unitToObserve] # the unit to be compared to all others
        keys = self.data.keys() #names of the units
        
        keyIter = iter(keys)
        shape = self.ax.shape
        print(shape)
        for row in range(shape[0]):
            for col in range(shape[1]):
                try:
                    key = next(keyIter)
                    compare_unit = self.data[key]

                    self.ax[row,col].plot(obs_unit,range(len(obs_unit)))
                    self.ax[row,col].plot(compare_unit,range(len(compare_unit)))
                    self.ax[row,col].set_title(key.split('_')[1].lower(),loc='center')
                    self.ax[row,col].set_xlim(0,self.max_time + 500)
                except StopIteration:
                    break
        self.fig.tight_layout()
        plt.show()

    def getMax(self,data):
        max_ = 0
        for k in data:
            for n in data[k]:
                if n > max_:
                    max_ = n
        return max_

g = Grapher('TERRAN_MEDIVAC')
g.plot()