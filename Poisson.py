1# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 18:17:46 2025

@author: logan
"""

debug = 0
debug1 = 0
debug2 = 0
debug3 = 0

epsilon = 8.854*10**(-12)

alpha = 1.0001


import numpy as np
import math
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--run1')
parser.add_argument('--run2')
parser.add_argument('--run3')
parser.add_argument('--run4')
parser.add_argument('--run5')

args = parser.parse_args()


def padMat2d(matIn):
    
    for i in range(len(matIn)):
        
        matIn[i] = [0] + matIn[i] + [0]
        
    tempList = []
    
    for i in range(len(matIn[0])):
        tempList.append(0)
        
    matOut = [tempList] + matIn + [tempList]
    
    return matOut
            

def catList(inList):
    cattedList = []
    for item in inList:
        cattedList += item
        
    return cattedList

class pointCharge:
    
    def __init__(self, charge, xPos, yPos, zPos=0):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.q = charge
        
    def getx(self):
        return self.xPos
    
    def gety(self):
        return self.yPos
    
    def getz(self):
        return self.zPos
    
    def getq(self):
        return self.q
    
class system:
    
    def __init__(self, dp, r=11, center=[0,0,0], z=False):
        self.dp = dp
        self.r = r
        self.center = center
        self.centerx = center[0]
        self.centery = center[1]
        self.centerz = center[2]
        
        self.delta = int(self.getr()/self.getdp()*2+1)
        self.hasz = z
        
        self.valList, self.coordList, self.rhoList = self.makeLists()
        self.chargeLocations = []
        
    def makeLists(self):
        valList = []
        coordList = []
        rhoList = []
        
        iterations = int(self.getr()/self.getdp())
        coords = list(range(int(-1*self.getr()/self.getdp()), int(self.getr()/self.getdp()+1)))
        self.coordrange = list(coords)
        
        for i in range(len(coords)):
            coords[i] = float(round(coords[i]*self.getdp(),2))
        
        itrange = list(range(iterations*2+1))
        self.itrange = list(itrange)
        
        if debug: print(f'coords: {coords}')
        if debug: print(f'itrange: {itrange}')
        
        
        for i in itrange:
            tempValList = []
            tempCoordList = []
            tempRhoList = []
            
            for j in itrange:
                
                if self.hasz:
                    tempValList.append([])
                    tempCoordList.append([])
                    tempRhoList.append([])
                
                    for k in itrange:
                        tempValList[j].append(0)
                        tempCoordList[j].append([coords[i], coords[j], coords[k]])
                        tempRhoList.append(0)
                
                else:
                    tempValList.append(0)
                    tempCoordList.append([coords[i], coords[j]])
                    tempRhoList.append(0)
                    
            valList.append(tempValList)
            coordList.append(tempCoordList)
            rhoList.append(tempRhoList)
            
        if debug: (print(coordList))
        if debug: print(valList)
            
        return valList, coordList, rhoList
    
    def getcoordrange(self):
        return self.coordrange
    
    def getitrange(self):
        return self.itrange
            
    def getdp(self):
        return self.dp
        
    def getr(self):
        return self.r
    
    def getcenter(self):
        return self.center
    
    def getcenterx(self):
        return self.centerx
    
    def getcentery(self):
        return self.centery
    
    def getcenterz(self):
        return self.centerz
    
    def getdelta(self):
        return self.delta
    
    def getValList(self):
        return self.valList
    
    def setChargeLocation(self, coords):
        self.chargeLocations.append(coords)
    
    def con2abscoords(self, coords):
        if self.hasz:
            pass
        else:
            valList = self.getValList()
            coordList = self.getCoordList()
            
            cattedCoords = catList(coordList)
            index = cattedCoords.index([coords[0], coords[1]])
        
            listxNum = index//self.getdelta()
            listyNum = index % self.getdelta()
            
            return [listxNum, listyNum]
    
    def setValInList(self, coords, val):
        if self.hasz:
            self.valList[coords[0]][coords[1]][coords[2]] = val
        else:
            self.valList[int(coords[0])][int(coords[1])] = val
            
    def setRhoInList(self, coords, rho):
        if self.hasz:
            self.rhoList[coords[0]][coords[1]][coords[2]] = rho
        else:
            self.rhoList[int(coords[0])][int(coords[1])] = rho
    
    def getCoordList(self):
        return self.coordList
    
    def getRhoList(self):
        return self.rhoList
    
    def __str__(self):
        vals = self.vals2str()
        
        for i in range(self.getdelta()): vals[i]=' '.join(vals[i])
        if debug: print(vals)
        vals = '\n'.join(vals)
        return vals
    
    def vals2str(self):
        if self.hasz:
            pass
        else:
            valList = list(self.getValList())
            strList = list(valList)
            
            for i in range(self.getdelta()):
                for j in range(self.getdelta()):
                    strList[i][j] = str(float(strList[i][j]))
        return strList
    
    def vals2float(self):
        if self.hasz:
            pass
        else:
            valList = list(self.getValList())
            floatList = list(valList)
            
            for i in range(self.getdelta()):
                for j in range(self.getdelta()):
                    floatList[i][j] = float(floatList[i][j])
        return floatList
    
    
    def placePointCharge(self, *pCharge):
        valList = self.getValList()
        coordList = self.getCoordList()
        
        cattedCoords = catList(coordList)
        
        if self.hasz:
            pass
        else:
            for p in pCharge:
                index = cattedCoords.index([p.getx(), p.gety()])
            
                listyNum = index//self.getdelta()
                listxNum = index % self.getdelta()
            
                if debug: print(listxNum)
                if debug: print(listyNum)
            
                self.setRhoInList([listxNum, listyNum], p.getq()/(self.getdp()**2))
                self.setChargeLocation([listxNum, listyNum])
                
            
    def singleCellJacobi(self, coords):
        if self.hasz:
            pass
        else:
            
            
            valList = self.getValList()
            
            newCoords = self.con2abscoords(coords)
            
            xPos = int(newCoords[0])
            yPos = int(newCoords[1])
        
            compSum = 0
            
            #if debug: print(f'singleCellJacobi valList[xPos][yPos]={valList[xPos][yPos]}')
            
            compSum = float(valList[xPos+1][yPos]) + compSum
            compSum = float(valList[xPos-1][yPos]) + compSum
            compSum = float(valList[xPos][yPos+1]) + compSum
            compSum = float(valList[xPos][yPos-1]) + compSum
            
            #if debug: print(f'compSum = {valList[xPos][yPos]}*({self.getdp()}**2)/{epsilon} + {compSum}')
            
            compSum = compSum + float(self.getRhoList()[xPos][yPos]*(self.getdp()**2)) #/epsilon
            
            newVal = compSum/4
            
            if debug1: print(f'did jacobi at cell ({xPos}, {yPos}): J={compSum}')
            if debug1: print(f'Neighbors are: ({xPos+1}, {yPos})-{valList[xPos+1][yPos]}, ({xPos-1}, {yPos})-{valList[xPos-1][yPos]}, ({xPos}, {yPos+1})-{valList[xPos][yPos+1]}, ({xPos}, {yPos-1})-{valList[xPos+1][yPos-1]}')
            
            return newVal
            
        
    def jacobi(self, rDisc=10):
        coordList = self.getCoordList()
        
        if debug1: print(self.getcoordrange())
        if debug1: print(self.getitrange())
        
        if self.hasz:
            pass
        else:
            newValList = []
            
            for i in self.getitrange()[1:-1]:
                tempNewValList = []
                for j in self.getitrange()[1:-1]:
                    if debug1: print(f'tried jacobi at ({i},{j})')
                    if ((coordList[i][j][0]**2+coordList[i][j][1]**2)**(0.5)>=rDisc):
                        tempNewVal = 0
                        if debug1: print(f'jacobi at {i},{j} is outside boundary')
                    else:
                        tempNewVal = self.singleCellJacobi(coordList[i][j])
                        
                    if debug2: print(f'ran jacobi for point ({coordList[i][j][0]}, {coordList[i][j][1]})')
                        
                    tempNewValList.append(tempNewVal)
                newValList.append(tempNewValList)
                #if debug: print('did Jacobi')
            self.valList = padMat2d(newValList)
                    
    def plotVals(self, colormap='bwr', cont=True):
        
        valList = self.vals2float()
        coords = list(range(int(-1*self.getr()/self.getdp()), int(self.getr()/self.getdp()+1)))
        
        if self.hasz:
            print('dear god why')
        else:
            plt.imshow(valList, cmap=colormap, extent=[-1*self.getr(), self.getr(), -1*self.getr(), self.getr()])
            
            if cont:
                plt.contour(coords, coords, valList)
            
    
    def jacobiNtimes(self, n, breakWhenCon=False, tol=0.01, rDisc = 10):
        
        coordList = self.getCoordList()
            
        valsAreClose = False
        hasConverged = False
        
        conVal = 'Did not converge'
        
        for k in range(n):
            
            valList = self.getValList()
            newValList = []
            valsAreClose = True
            
            for i in self.getitrange()[1:-1]:
                tempNewValList = []
                for j in self.getitrange()[1:-1]:
                    
                    if ((coordList[i][j][0]**2+coordList[i][j][1]**2)**(0.5)>=rDisc):
                        tempNewVal = 0
                        #if debug1: print(f'jacobi at {i},{j} is outside boundary')
                    else:
                        tempNewVal = self.singleCellJacobi(coordList[i][j])
                        
                    if not math.isclose(tempNewVal, valList[i][j], rel_tol=tol):
                        valsAreClose = False
                    #if debug2: print(f'ran jacobi for point ({coordList[i][j][0]}, {coordList[i][j][1]})')
                        
                    tempNewValList.append(tempNewVal)
                newValList.append(tempNewValList)
                #if debug: print('did Jacobi')
            
            if hasConverged:
                print(f'{round((k+1)/n*100, 3)}% done [Converged at {conVal}]')
            else:
                print(f'{round((k+1)/n*100, 3)}% done')
            
            if (not hasConverged) and valsAreClose:
                hasConverged = True
                print(f'Converged at iteration: {k}')
                conVal = k
            
            if debug3: print(f'valList: {valList}')
            if debug3: print(f'tempNewValList: {tempNewValList}')
            if debug3: print(valsAreClose)
            self.valList = padMat2d(newValList)
            
            if breakWhenCon and hasConverged:
                break
            
        print(f'Converged at k={conVal}')
        
        
    def singleCellSOR(self, coords):
        if self.hasz:
            pass
        else:
            
            
            valList = self.getValList()
            
            newCoords = self.con2abscoords(coords)
            
            xPos = int(newCoords[0])
            yPos = int(newCoords[1])
        
            compSum = 0
            
            #if debug: print(f'singleCellJacobi valList[xPos][yPos]={valList[xPos][yPos]}')
            
            compSum = float(valList[xPos+1][yPos]) + compSum
            compSum = float(valList[xPos-1][yPos]) + compSum
            compSum = float(valList[xPos][yPos+1]) + compSum
            compSum = float(valList[xPos][yPos-1]) + compSum
            
            #if debug: print(f'compSum = {valList[xPos][yPos]}*({self.getdp()}**2)/{epsilon} + {compSum}')
            
            compSum = compSum + float(self.getRhoList()[xPos][yPos]*(self.getdp()**2)) #/epsilon
            
            newVal = compSum/4*alpha + (1-alpha)*(valList[xPos][yPos])
            
            if debug1: print(f'did SOR at cell ({xPos}, {yPos}): J={compSum}')
            if debug1: print(f'Neighbors are: ({xPos+1}, {yPos})-{valList[xPos+1][yPos]}, ({xPos-1}, {yPos})-{valList[xPos-1][yPos]}, ({xPos}, {yPos+1})-{valList[xPos][yPos+1]}, ({xPos}, {yPos-1})-{valList[xPos+1][yPos-1]}')
            
            return newVal
        
        
    def SOR(self, rDisc=10):
        coordList = self.getCoordList()
        
        if debug1: print(self.getcoordrange())
        if debug1: print(self.getitrange())
        
        if self.hasz:
            pass
        else:
            newValList = []
            
            for i in self.getitrange()[1:-1]:
                tempNewValList = []
                for j in self.getitrange()[1:-1]:
                    if debug1: print(f'tried SOR at ({i},{j})')
                    if ((coordList[i][j][0]**2+coordList[i][j][1]**2)**(0.5)>=rDisc):
                        tempNewVal = 0
                        if debug1: print(f'SOR at {i},{j} is outside boundary')
                    else:
                        tempNewVal = self.singleCellSOR(coordList[i][j])
                        
                    if debug2: print(f'ran SOR for point ({coordList[i][j][0]}, {coordList[i][j][1]})')
                    
                    tempNewValList.append(tempNewVal)
                newValList.append(tempNewValList)
                #if debug: print('did Jacobi')
            self.valList = padMat2d(newValList)
                
        
    def SORNtimes(self, n, breakWhenCon=False, tol=0.01, rDisc = 10):
        
        coordList = self.getCoordList()
            
        valsAreClose = False
        hasConverged = False
        
        conVal = 'Did not converge'
        
        for k in range(n):
            
            valList = self.getValList()
            newValList = []
            valsAreClose = True
            
            for i in self.getitrange()[1:-1]:
                tempNewValList = []
                for j in self.getitrange()[1:-1]:
                    
                    if ((coordList[i][j][0]**2+coordList[i][j][1]**2)**(0.5)>=rDisc):
                        tempNewVal = 0
                        #if debug1: print(f'SOR at {i},{j} is outside boundary')
                    else:
                        tempNewVal = self.singleCellSOR(coordList[i][j])
                        
                    if not math.isclose(tempNewVal, valList[i][j], rel_tol=tol):
                        valsAreClose = False
                    #if debug2: print(f'ran SOR for point ({coordList[i][j][0]}, {coordList[i][j][1]})')
                        
                    tempNewValList.append(tempNewVal)
                newValList.append(tempNewValList)
                #if debug: print('did SOR')
            
            if hasConverged:
                print(f'{round((k+1)/n*100, 3)}% done [Converged at {conVal}]')
            else:
                print(f'{round((k+1)/n*100, 3)}% done')
            
            if (not hasConverged) and valsAreClose:
                hasConverged = True
                print(f'Converged at iteration: {k}')
                conVal = k
            
            if debug3: print(f'valList: {valList}')
            if debug3: print(f'tempNewValList: {tempNewValList}')
            if debug3: print(valsAreClose)
            self.valList = padMat2d(newValList)
            
            if breakWhenCon and hasConverged:
                break
            
        print(f'Converged at k={conVal}')  
            
    
    
    
def make2pointCharges(a, q):
    cp = pointCharge(q, float(round(a/2, 2)), float(0), 0)
    cn = pointCharge(q*-1, float(round(-1*a/2, 2)), float(0), 0)
    return cp, cn

def test1():
    sys = system(0.1)
    
def test2():
    sys = system(1)
    cp, cn = make2pointCharges(2, 1)
    print(cp.getx())
    sys.placePointCharge(cp)
    print(sys)
    
def test3():
    list1 = [['a', 1], ['b', 2], ['c', 3], ['d', 4]]
    cattedList = catList(list1)
    print(cattedList)
    
def test4():
    sys = system(1)
    cp, cn = make2pointCharges(2, 1)
    
    sys.placePointCharge(cp)
    
    print(sys)
    
    for i in range(1000):
        sys.jacobi()
    
    print(sys)
    
    print(sys.getValList())
    
    sys.plotVals()
    
def test5():
    sys = system(1, r=10)
    cp, cn = make2pointCharges(2, 1)
    
    sys.placePointCharge(cp)
    
    print(sys)
    
    sys.singleCellJacobi([0,0])
    
def test6():
    sys = system(1, 5)
    coords = [3, 4]
    newCoords = sys.con2abscoords(coords)
    print(sys)
    print(newCoords)
    
def test7():
    list1 = [[1, 2], [3, 9]]
    
    newList = padMat2d(list1)
    
    print(newList)
    
def testf():
    sys = system(0.1)
    
    sis = system(0.5)
    
    cp, cn = make2pointCharges(2, 1)
    
    cp2 = pointCharge(5, 2, 3)
    cn2 = pointCharge(-3, 2, -4)
    cp3 = pointCharge(5, 2.2, -4.8)
    cn3 = pointCharge(-4, 1.6, 2.4)
    cp4 = pointCharge(10, -3.4, -2)
    cn4 = pointCharge(-4, -3.0, -1.8)
    cn5 = pointCharge(-6, -4.0, -2.4)
    cp5 = pointCharge(6, 0.4, 0.8)
    
    cn6 = pointCharge(-3, -2.2, 2.8)
    cn7 = pointCharge(-3, -2.6, 3.4)
    cn8 = pointCharge(-3, -2.0, 3.0)
    cn9 = pointCharge(-3, -2.8, 2.6)
    
    cp6 = pointCharge(10, -2.4, 3.0)
    
    #print(sys.getCoordList())
    
    sys.placePointCharge(cp, cn, cn2, cp2, cn3, cp3, cp4, cn4, cn5, cp5, cn6, cn7, cn8, cn9, cp6)
    sis.placePointCharge(cp, cn)
    
    numTimes = 3000
    
    sys.jacobiNtimes(numTimes, False)
        
    
    
    sys.plotVals('viridis')
    
def run2():
    sys = system(0.2)
    
    cp, cn = make2pointCharges(1.2, 1)
    
    numTimes = 100
    
    sys.placePointCharge(cp, cn)
    sys.SORNtimes(numTimes, False)
    
    sys.plotVals('viridis')
    
    
    

if __name__=='__main__':
    run2()
    
if args.run1:
    testf()
    pass

if args.run2:
    print('run not applicble')
    pass

if args.run3:
    run2()
    pass

if args.run4:
    print('run not applicble')
    pass

if args.run5:
    print('run not applicble')
    pass
