import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import tkinter as tk

import time

import logging

class PltUi():
    def __init__(self, frame, size = 1):
        #log
        self.logger = logging.getLogger('__name__')

        self.frame = frame
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.size = size
        self.setLabels("Temps [s]", "Valeur [?]")
        
        
       # self.line, = self.ax.plot([], [])
        
        self.lastRefresh = time.time()
        self.freq = 1

        self.maxNbValue = 100
        self.maxTime = 10
        self.x = np.array([])
        self.y = np.array([])

    def setXLabel(self, xLabel):
        self.xLabel = xLabel
        self.setGrid()
    
    def setYLabel(self, yLabel):
        self.yLabel = yLabel
        self.setGrid()
    
    def setLabels(self, xLabel, yLabel):
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.setGrid()   
    
    
    def setGrid(self) -> None:
        self.ax.set_xlabel(self.xLabel)
        self.ax.set_ylabel(self.yLabel)
        self.ax.grid(True)

        self.setSize(self.size)

    def setSize(self, val):
        self.lines = []
        for i in range(val):
            line, = self.ax.plot([], [])
            self.lines = np.append(self.lines, line)


    def update2(self,dt, value):
        for i in range(len(self.lines)):
            print
            #try :
            self.update(dt[i], value[i],self.lines[i])
            #except:
            #    print("aie caramba")
            
           
    def update(self,dt, value, line):
        #self.logger.debug("Update vaue de la courbe")
        if dt > 0:
            self.maxNbValue = int(self.maxTime/dt)
        
        x = line.get_data()[0]
        y = line.get_data()[1]

        

        if len(x) == 0:
            x = np.append(x, dt)
        else:
            x = np.append(x, x[-1] + dt)
        y = np.append(y, value)
        x = self.setLength(x)
        y = self.setLength(y)
        
        line.set_data(x, y)

            
            
    def updateUi(self):
        #self.logger.debug("Reset de l'affichage de la courbe")
        try:
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
        except:
            self.logger.debug("Shape Error")
    
    def isTimeOk(self) -> bool:
        elapsedTime = time.time() - self.lastRefresh
        if elapsedTime > (1/self.freq):
            self.lastRefresh = time.time()
            return True
        return False

    def setCourbe(self, t, y):
        self.ax.plot(t, y)

    def setLength(self, x):
        lx = len(x)
        if lx > self.maxNbValue:
            x = x[lx - self.maxNbValue:lx]
        return x
    
    def clear(self):
        """
        Efface tout les données
        """
        self.ax.clear()
        self.setGrid()



