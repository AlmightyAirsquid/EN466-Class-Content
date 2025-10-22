# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 17:22:42 2025

@author: logan
"""

import random
import matplotlib.pyplot as plt
import math

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--run1')
parser.add_argument('--run2')
parser.add_argument('--run3')
parser.add_argument('--run4')
parser.add_argument('--run5')

args = parser.parse_args()


numRands = 1000
sigma = 1

debug = 1

randomNumList = [] 

def makeRandList(numRands):
    randList = []
    for i in range(numRands):
        appendNum = random.random()
        randList.append(appendNum)
    return randList

def makeGaussDist(numRands):
    gaussXList = []
    gaussYList = []
    for i in range(numRands):
        vals = BoxMuller()
        gaussXList.append(vals[0])
        gaussYList.append(vals[1])
    if debug == 0: print([gaussXList, gaussYList])
    return [gaussXList, gaussYList]

def BoxMuller():
    randomR = (-2*math.log(random.random()))
    randomTheta = 2*math.pi*random.random()
    
    xVal = randomR*math.cos(randomTheta)
    yVal = randomR*math.sin(randomTheta)
    
    return [xVal,yVal]

def makeNsubdivisions(numList, nSubdivisions):
    
    newList = []
    if debug: print(f'numList length: {len(numList)}')
    if debug: print(f'number of Subdivisions: {nSubdivisions}')
    if debug: print(f'len(numList)/nSubdivisions={len(numList)/nSubdivisions}')
    xSpace = int(len(numList)/nSubdivisions)
    
    for i in range(nSubdivisions):
        newList.append(numList[i*xSpace:(i+1)*xSpace])
        
    return newList

def getAverage2dListVal(listIn):
    
    summedList = []
    
    for i in range(len(listIn)):
        summedList.append(sum(listIn[i])/len(listIn[i]))
    
    if debug: print(summedList)
    return summedList

def plotNsubdivisions(numList, nSubdivisions):
    
    newList = makeNsubdivisions(numList, nSubdivisions)
    
    summedList = getAverage2dListVal(newList)
    
    xSpace = []
    for i in range(nSubdivisions):
        xSpace.append(int(i*len(numList)/nSubdivisions))
    ySpace = list(summedList)
    
    plt.plot(xSpace, ySpace)
    plt.axis([0,len(numList),0.3,0.7])
    
def PlotNsubdivisions(numList, nSubdivisions):
    plt.hist(numList, bins=nSubdivisions)
    
def plotVals(xList, yList):
    
    plt.plot(xList, yList)
    

def testA():
    randList = makeRandList(numRands)
    newList = makeNsubdivisions(randList, 10)
    
    print(randList)
    print()
    print(newList)
    
def run1(numRands, *subdivisions):
    
    numList = makeRandList(numRands)
    
    for subdivision in subdivisions:
        PlotNsubdivisions(numList, subdivision)
        
def run2(numRands, *subdivisions):
    
    for subdivision in subdivisions:
        numList = makeGaussDist(numRands*subdivision)
        PlotNsubdivisions(numList[0], subdivision)
        
def test1():
    run1(1000000, 10, 20, 50, 100)
    
def test2():
    run2(numRands, 10, 20, 50, 100)
    
def test3():
    numList = makeGaussDist(1000)
    plotVals(numList[0], numList[1])
        
    

if __name__=='__main__':
    if debug: testA()
    random.seed(69)
    run1(numRands)
    
if args.run1:
    run1()
    pass

if args.run2:
    run2()
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
