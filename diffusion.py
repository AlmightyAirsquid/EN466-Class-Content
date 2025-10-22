# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:07:23 2025

@author: logan
"""

D = 2


debug = 1

import math
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--RUN')

args = parser.parse_args()

e = math.e
pi = math.pi

class grid1D:
    
    def __init__(self, r=10, dx=0.1, dt=0.001, t=0):
        self.r = r
        self.dx = dx
        self.dt = dt
        self.t = t
        self.gridVals = self.makeZeros()
        self.gridCoords = self.makegridCoords()
        
    def getr(self):
        return self.r
    
    def getdx(self):
        return self.dx
    
    def getdt(self):
        return self.dt
    
    def getgridVals(self):
        return self.gridVals
    
    def gett(self):
        return self.t
    
    def inct(self):
        self.t = self.t + self.dt
    
    def getgridCoords(self):
        return self.gridCoords
    
    def setgridVal(self, val, xPos):
        self.gridVals[xPos]=val
        
    def __str__(self):
        newVals = self.makeListStr(self.getgridVals())
        return ' '.join(newVals)
        
    def makegridCoords(self):
        gridVals = []
        
        for i in range(int(self.getr()/self.getdx())):
            gridVals.append(round(self.getdx()*(i)-self.getr()/2, 3))
        
        gridVals.append(round(self.getr()/2, 3))
        return gridVals
    
    def makeListStr(self, inList):
        newList = []
        
        for i in range(len(inList)):
            newList.append(str(inList[i]))
        
        return newList
    
    def makeZeros(self):
        gridCoords = []
        
        for i in range(int(self.getr()/self.getdx())):
            gridCoords.append(round(0, 3))
        
        gridCoords.append(round(0, 3))
        return gridCoords
    
    def populate(self, val, coord=0.0):
        
        xPos = self.getgridCoords().index(coord)
        self.setgridVal(val/self.getdx(), xPos)
        
    def diffuse(self):
        
        newValList = [round(0,3)]
        gridVals = self.getgridVals()
        
        for i in range(1, len(self.getgridCoords())-1):
            coeff = D*self.getdt()/(self.getdx()**2)
            appendVal = gridVals[i] + coeff*(gridVals[i-1]-2*gridVals[i]+gridVals[i+1])
            
            newValList.append(appendVal)
        
        newValList.append(round(0,3))
        
        self.gridVals = newValList
        
    def diffuseNseconds(self, seconds, plot=False, plotBar=False, plotGauss=False):
        itLength = int(seconds/self.getdt())
        for i in range(itLength):
            self.diffuse()
            print(f'{(i+1)/itLength*100}% complete.')
            self.inct()
        if plot: self.plotVals()
        if plotBar: self.plotBar()
        if plotGauss: self.plotGauss()
        
        
    def plotBar(self):
        valList = self.getgridVals()
        gridCoords = self.getgridCoords()
        plt.bar(gridCoords, valList)
        
    def plotVals(self):
        valList = self.getgridVals()
        gridCoords = self.getgridCoords()
        
        plt.plot(gridCoords, valList)
        
    def plotGauss(self):
        gridCoords = self.getgridCoords()
        yList = []
        for coord in gridCoords:
            sigma = math.sqrt(2*D*self.gett())
            if sigma ==0:
                exp = 0
            else:
                exp = -1*(coord**2)/(2*(sigma**2))
            den = math.sqrt(2*(sigma**2))
            rho = 5.642/den*e**(exp)
            
            yList.append(rho)
        plt.plot(gridCoords, yList)
        
    def plotNtimes(self, *seconds, plot=False, plotBar=False, plotGauss=False):
        maxTime = max(seconds)
        itLength = int(maxTime/self.getdt())
        for i in range(itLength):
            self.diffuse()
            print(f'{(i+1)/itLength*100}% complete')
            if debug: print(self.gett())
            
            for second in seconds:
                if math.isclose(second, self.gett()):
                    if plot: self.plotVals()
                    if plotBar: self.plotBar()
                    if plotGauss: self.plotGauss()
            
            self.inct()
        

def test1():
    grid = grid1D(r=2, dx=0.1)
    print(grid)
    
    grid.populate(8)
    
    print(grid)
    
def test2():
    grid = grid1D(r=1)
    
    grid.populate(10)
    
    print(grid)
    
    grid.diffuse()
    
    print(grid.getgridVals())
    
def test3():
    grid = grid1D(r=50)
    
    grid.populate(10)
    
    grid.diffuseNseconds(5, plot=True, plotGauss=True, plotBar=True)
    
    print(grid.getgridVals())
    
def test4():
    grid = grid1D(r=50)
    grid.populate(10)
    grid.diffuseNseconds(10)
    
    grid.plotVals()
    grid.plotGauss()
    
    
def test5():
    grid = grid1D(r=50)
    grid.populate(10)
    
    grid.plotNtimes(.1, 2, 5, 10, 20, plotBar=True, plotGauss=True)

    
    
if __name__=='__main__':
    if debug: test2()
    test4()
    
if args.RUN:
    
    if args.RUN==1:
        print('run not applicble')
        pass
    
    if args.RUN==2:
        
        test4()
        
        pass
    
    if args.RUN==3:
        print('run not applicble')
        pass
    
    if args.RUN==4:
        print('run not applicble')
        pass
    
    if args.RUN==5:
        print('run not applicble')
        pass
