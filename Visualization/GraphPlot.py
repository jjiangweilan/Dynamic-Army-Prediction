import matplotlib.pyplot as plt
import math
#signiture to pass dyntatic detection
def Preprocessor():
    pass

class Grapher:
    "graph processed data \
    the graph is designed to better observe the \
    relation of one unit with all other units\
    "

    def __init__(self,unitToObserve):
        self.data = {} #TO_DO: data to plot
        self.unitToObserve = unitToObserve
        self.totalUnits = len(self.data["p1"]["units"])

        #creat the sublot
        COLS = 6
        rows = math.ceil(self.totalUnits/float(COLS))
        self.fig, self.ax = plt.subplots(nrows=rows, ncols=COLS)
    
    def plot(self):
        obs_unit = self.data["p1"]["units"][self.unitToObserve] # the unit to be compared to all others
        keys = self.data["p1"]["units"].keys() #names of the units
        
        keyIter = iter(keys)
        for row in self.ax:
            for col in row:
                try:
                    key = next(keyIter)
                    compare_unit = self.data["p1"]["units"][key]

                    col.plot(range(len(obs_unit)), obs_unit)
                    col.plot(range(len(compare_unit)), compare_unit)
                    col.set_title(key,loc='center')
                except StopIteration:
                    break