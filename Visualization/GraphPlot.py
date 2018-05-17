import matplotlib.pyplot as plt
import math
#signiture to pass dyntatic detection
def Preprocessor():
    pass

class grapher:
    "graph processed data \
    the graph is designed to better observe the \
    relation of one unit with all other units\
    "

    def __init__(self,unitToObserve):
        self.data = {} #TO_DO: data to plot
        self.unitToObserve = unitToObserve

        totalUnits = len(self.data["units"])
        COLS = 6
        rows = math.ceil(totalUnits/float(COLS))
        fig, ax = plt.subplot(nrows=rows, ncols=COLS)
    
    def plot(self):
        self.data["p1"]["units"][self.unitToObserve]
        for row in ax:
            for col in row:
                col.plot #TO_DO