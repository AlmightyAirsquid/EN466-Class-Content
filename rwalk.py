# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 13:16:07 2025

@author: logan
"""

from Gases import Mover
import random
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--RUN')

args = parser.parse_args()

walkNum = 400

mover = Mover('Timmy', 0, 0)

def moveNtimes(mover, numWalks):
    
    mover.setPos(0, 0)
    
    for i in range(numWalks):
        mover.randomMove()
        
    xPos=mover.getxPos()
    xPosSquare=mover.getxPos()**2
    sqMag = mover.getMagnitude()**2
    
    mover.setPos(0, 0)
    
    return [xPos, xPosSquare, sqMag]

def moveNtimesNtimes(mover, ni, nf, nTimes):
    
    normalList = []
    squareList = []
    nRange = range(ni, nf)
    
    for n in nRange:
        currentSum = [0,0]
        for i in range(nTimes):
            moveList = moveNtimes(mover, n)
            currentSum[0] += moveList[0]
            currentSum[1] += moveList[1]
        
        currentSum[0] = currentSum[0]/nTimes
        currentSum[1] = currentSum[1]/nTimes
        normalList.append(currentSum[0])
        squareList.append(currentSum[1])
    
    return [nRange, normalList, squareList]

def plotMovement(mover, ni, nf, nTimes):
    
    valList = moveNtimesNtimes(mover, ni, nf, nTimes)
    
    plt.plot(valList[0], valList[1])
    plt.plot(valList[0], valList[2])
    plt.show()
    
def plotMag(mover, ni, nf, nTimes):
    valList = moveNtimesNtimes(mover, ni, nf, nTimes)
    
    plt.plot(valList[0], valList[2])
    
def testA():
    print(f'{mover.getval()} is going on a walk {walkNum} times! {mover.getval()} is starting at ({mover.getxPos()}, {mover.getyPos()}).')
    
    for i in range(walkNum):
        mover.randomMove()
        
    print(f'{mover.getval()} is ending his walk at ({mover.getxPos()}, {mover.getyPos()}) with a magnitude of {mover.getMagnitude()**2}')


if __name__=='__main__':
    
    plotMovement(mover, 3, 100, 10**3)
    
if args.RUN:
    
    if args.RUN==1:
        plotMovement(mover, 3, 100, 10**3)
        pass
    
    if args.RUN==2:
        
        plotMag(mover, 3, 100, 10**3)
        
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
