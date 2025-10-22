# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 16:28:18 2025

@author: logan
"""

debug = 0

debugRandomMove = 1

import random
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import numpy as np

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--run1')
parser.add_argument('--run2')
parser.add_argument('--run3')
parser.add_argument('--run4')
parser.add_argument('--run5')

args = parser.parse_args()

Ntimes = 10



class Mover:
    
    def __init__(self, val, xPos,yPos):
        self.val = val
        self.xPos = xPos
        self.yPos = yPos
        
    def getval(self):
        return self.val
        
    def getxPos(self):
        return self.xPos
    
    def getyPos(self):
        return self.yPos
    
    def getPos(self):
        return [self.getxPos(), self.getyPos()]
    
    def setxPos(self, setVal):
        self.xPos = setVal
        
    def setyPos(self, setVal):
        self.yPos = setVal
        
    def setPos(self, setxVal, setyVal):
        self.setxPos(setxVal)
        self.setyPos(setyVal)
        
    def movex(self, moveAmount=1):
        self.setxPos(self.getxPos()+moveAmount)
        
    def movey(self, moveAmount=1):
        self.setyPos(self.getyPos()+moveAmount)
        
    def randomMove(self, moveAmount=1):
        leftOrRight = random.randint(0, 1)
        posOrNeg = random.randint(0, 1)*2-1
        if leftOrRight: self.movex(moveAmount*posOrNeg)
        else: self.movey(moveAmount*posOrNeg)
        
    def getMagnitude(self):
        return (self.getxPos()**2+self.getyPos()**2)**(0.5)
        
    def __str__(self):
        return self.getval()
    
    def __repr__(self):
        return f'("{self.getval()}", xPos: {self.getxPos()}, yPos: {self.getyPos()})'
    
class Grid:
    
    def __init__(self, xDim, yDim):
        self.xDim = xDim
        if debug: print(f'xDim is {xDim}')
        self.xRange = list(range(xDim))
        if debug: print(self.getxRange())
        self.yDim = yDim
        if debug: print(f'yDim is {yDim}')
        self.yRange = list(range(yDim))
        if debug: print(self.getyRange())
        
        self.makeselfList()
        
        if debug: print(self.getList())
        self.moverList = []
        
    def makeselfList(self):
        selfList = []
        for j in self.getyRange(): 
            xList = []
            for i in self.getxRange(): 
                xList.append(0)
            selfList.append(xList)
        self.selfList = list(selfList)
        
        return selfList
        
    def getList(self):
        return self.selfList
    
    def getxDim(self):
        return self.xDim
    
    def getxRange(self):
        return self.xRange
    
    def getyDim(self):
        return self.yDim
    
    def getyRange(self):
        return self.yRange
    
    def getMoverList(self):
        return self.moverList
    
    def checkList4Mover(self, mover):
        moverList = self.getMoverList()
        for i in moverList:
            if self.checkLocation4Mover(mover, moverList[i].getxPos(), moverList.getyPos()):
                return 1
        return 0

    def checkLocation4Mover(self, xPos, yPos):
        moverList = self.getMoverList()
        for mover in moverList:
            if ((mover.getxPos() == xPos) and (mover.getyPos() == yPos)): return 1
        return 0
    
    def checkLocation4Empty(self, xPos, yPos):
        moverList = self.getMoverList()
        for mover in moverList:
            if ((mover.getxPos() == xPos) and (mover.getyPos() == yPos)): return 0
        return 1
    
    def addMover(self, mover, check=0):
        if check:
            if self.checkList4Mover(mover):
                raise Exception('Your mover tried to occupy an already occupied space dipshit.')
        self.moverList.append(mover)
        pass
    
    def con2str(self):
        selfList = self.makeselfList()
        strList = list(selfList)
        for i in self.getxRange():
            for j in self.getyRange():
                if debug: print(f'({i},{j})')
                strList[j][i]=str(selfList[j][i])
        return strList
    
    def back2int(self, matIn):
        selfList = matIn
        intList = list(selfList)
        for i in self.getxRange():
            for j in self.getyRange():
                intList[j][i]=int(selfList[j][i])
        return intList
        
    def __repr__(self):
        vals = self.con2str()
        for i in self.getxRange(): vals[i]=' '.join(vals[i])
        vals = '\n'.join(vals)
        return vals
    
    def __str__(self):
        vals = list(self.con2str())
        moverList = self.getMoverList()
        if debug: print(self.getyRange())
        
        if debug: print(f'Mover List is: {self.getMoverList()}')
        
        for mover in moverList: 
            vals[mover.getyPos()][mover.getxPos()]=mover.getval()
        
        for i in self.getyRange(): vals[i]=' '.join(vals[i])
        if debug: print(vals)
        vals = '\n'.join(vals)
        return vals
        
    def populate(self, species, yStart, yStop, xStart=0, xStop=None):
        if xStop == None: xStop = self.getxDim()
        xPopRange=range(xStart, xStop)
        yPopRange=range(yStart, yStop)
        
        for i in xPopRange:
            for j in yPopRange:
                mover = Mover(species, i, j)
                self.addMover(mover)
        
        if debug: print(self.getMoverList())
        
    def getopenAdjacentSpots(self, mover):
        xPos = mover.getxPos()
        yPos = mover.getyPos()
        openSpotList = []
        if (self.checkLocation4Empty(xPos+1, yPos) and (xPos != (self.getxDim()-1))):
            openSpotList.append([xPos+1, yPos])
        if self.checkLocation4Empty(xPos-1, yPos) and (xPos != 0):
            openSpotList.append([xPos-1, yPos])
        if self.checkLocation4Empty(xPos, yPos+1) and (yPos != (self.getyDim()-1)):
            openSpotList.append([xPos, yPos+1])
        if self.checkLocation4Empty(xPos, yPos-1) and (yPos != 0):
            openSpotList.append([xPos, yPos-1])
        
        return openSpotList
        pass
    
    def randomMove(self, mover):
        openSpotList = list(self.getopenAdjacentSpots(mover))
        numSpots = len(openSpotList)
        if numSpots == 0: return 0
        
        randomIndex = random.randint(0, numSpots-1)
        
        mover.setxPos(openSpotList[randomIndex][0])
        mover.setyPos(openSpotList[randomIndex][1])
        
    def makeImage(self):
        pass
        
def testA():
    pass
        
def testB():
    Mat = Grid(4,6)
    GasA = Mover('A', 3, 4)

    #print(Mat)

    #print()

    #Mat.addMover(GasA)
    Mat.populate('A', 0, 5)
    
    print(Mat)

    #Mat.populate('P', 0, 19)

    #Mat.populate('M', 40, 60)

    #print(Mat)

    #print(Mat.checkLocation4Mover(3, 4))
    #print(Mat.checkLocation4Empty(3, 4))
    print(Mat.getopenAdjacentSpots(GasA))
    Mat.makeImage()
    
    for i in range(Ntimes):
        print(GasA.getPos())
        Mat.randomMove(GasA)
        print(GasA.getPos())
        print(Mat)
    pass
    
if __name__=='__main__':
        
    random.seed(420)
    
if args.run1:
    testB()
    pass

if args.run2:
    print('run not applicble')
    pass

if args.run3:
    print('run not applicble')
    pass

if args.run4:
    print('run not applicble')
    pass

if args.run5:
    print('run not applicble')
    pass
