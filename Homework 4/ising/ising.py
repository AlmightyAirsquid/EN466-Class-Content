# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 13:57:02 2025

@author: logan
"""

import datetime
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import imageio.v2 as iio
import glob
import os
import argparse




#random.seed(67)

e=math.e
J=1.5
kb=1
#T=0.001

debug1 = 0

class grid:
    def __init__(self, x, y=0):
        self.x = x
        if y:
            self.y=y
        else:
            self.y=self.x

        self.xrange = range(self.getx())
        self.yrange = range(self.gety())

        self.grid = self.makeGrid()
        self.randomPopulate()
        self.t = 0

        self.initialGrid = np.array(self.getgrid())

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getxrange(self):
        return self.xrange

    def getyrange(self):
        return self.yrange

    def getgrid(self):
        return self.grid

    def setgridcoord(self,x,y,val):
        self.grid[x][y]=val

    def gett(self):
        return self.t

    def reset(self):
        self.grid = self.initialGrid.copy()
        self.t = 0

    def flip(self,x,y):
        self.grid[x][y]=-1*self.grid[x][y]

    def makeGrid(self):
        grid = np.zeros((self.getx(),self.gety()), dtype=int)
        return grid

    def plot(self, save=False,T=1):
        plt.imshow(self.getgrid())
        if save:
            plt.savefig(f'gridplot_t{self.gett()}_T{T}_{self.getx()}x{self.gety()}grid.png')
            plt.close()

    def randomPopulate(self):
        #grid = self.getgrid()
        xrange = self.getxrange()
        yrange = self.getyrange()

        for x in xrange:
            for y in yrange:
                val = random.randint(0, 1)*2-1
                self.setgridcoord(x, y, val)

    def neighborSum(self,x,y):
        grid=self.getgrid()

        if x !=0:
            xstart = x-1
        else:
            xstart = x

        if y !=0:
            ystart = y-1
        else:
            ystart = 0

        xSumIndex = xstart
        ySumIndex = ystart

        sumCount = 0

        debugList = []

        while xSumIndex <= (x+1) and xSumIndex <= (self.getx()-1):

            if y !=0:
                ystart = y-1
            else:
                ystart = 0
            ySumIndex = ystart

            while ySumIndex <= (y+1) and ySumIndex <= (self.gety()-1):

                if (xSumIndex==x)and(ySumIndex==y)or(xSumIndex!=x)and(ySumIndex!=y):
                    pass
                else:
                    sumCount =sumCount + grid[xSumIndex][ySumIndex]
                    if debug1:
                        debugList.append(grid[xSumIndex][ySumIndex])

                ySumIndex = ySumIndex+1

            xSumIndex=xSumIndex+1

        if debug1:
            print(debugList)

        return sumCount

    def hamiltonian(self,x,y,T=1):
        summedVal = self.neighborSum(x, y)
        grid = self.grid
        deltaE = 2*J*grid[x][y]*summedVal

        return deltaE

    def calcNewVal(self,x,y,T=1):
        E = self.hamiltonian(x, y,T)
        grid = self.getgrid()

        if E<0:
            return -1*grid[x][y]
        else:
            prob=e**(-1*E/kb/T)
            num = random.random()

            if num > prob:
                return grid[x][y]
            else:
                return -1*grid[x][y]

    def ising(self,T=1):
        #xrange = self.getxrange()
        #yrange = self.getyrange()
        #newgrid = self.makeGrid()
        #grid = self.getgrid()
        randx=random.randint(0, self.getx()-1)
        randy=random.randint(0, self.gety()-1)

        self.grid[randx][randy]=self.calcNewVal(randx, randy,T)

        #self.grid = newgrid
        self.t +=1

    def similtaneousIsing(self,T=1):
        xrange = self.getxrange()
        yrange = self.getyrange()
        newgrid = self.makeGrid()
        #grid = self.getgrid()

        for x in xrange:
            for y in yrange:
                newgrid[x][y]=self.calcNewVal(x, y,T)

        self.grid = newgrid
        self.t +=1

    def isingNtimes(self,N,T=1):
        for i in range(N):
            self.ising()
            print(f'{(i+1)/N*100}% done')

    def out(self):
        print(self.getgrid())

    def mp4ising(self,N,T=1,f=25, run=1, maxRun=1,fpn=1000):
        self.plot(True,T)

        for i in range(N):
            self.ising(T)

            if self.gett()%fpn==0:
                self.plot(True,T)
            print(f'{round((i+1)/N*100,2)}% done run {run} of {maxRun} for x={self.getx()}')
        
        
        files=sorted(glob.glob(f'gridplot_t*_T{T}_{self.getx()}x{self.gety()}grid.png'), key=os.path.getmtime)

        with iio.get_writer(f'ising_t{self.gett()}_T{T}_{f}fps_{N}N_{self.getx()}x{self.gety()}grid.mp4', fps=f) as writer:
            for file in files:
                image=iio.imread(file)
                writer.append_data(image)

    def mp4wTs(self, N, Tlist,f=25, fpn=1000):
        maxRun=len(Tlist)
        run = 1

        for T in Tlist:
            self.mp4ising(N,T,f,run,maxRun,fpn)
            self.reset()
            run +=1

tlist = [0.01,0.1,1,10,100,1000]

def mp4wTsXs(Xlist,Tlist,N=[400], fps=[25],fpn=[1000]):
    
    if (len(fps)==1)and(len(N)==1):
        for X in Xlist:
            g = grid(X)
            g.mp4wTs(N[0], Tlist, fps[0],fpn[0])
    if (len(fps)>1)and(len(N)==1):
        for i in range(len(Xlist)):
            g = grid(Xlist[i])
            g.mp4wTs(N[0],Tlist,fps[i],fpn[i])
    if (len(fps)==1)and(len(N)>1):
        for i in range(len(Xlist)):
            g = grid(Xlist[i])
            g.mp4wTs(N[i],Tlist,fps[0],fpn[0])
    if (len(fps)>1)and(len(N)>1):
        for i in range(len(Xlist)):
            g = grid(Xlist[i])
            g.mp4wTs(N[i],Tlist,fps[i],fpn[i])

def setup():
    h = grid(25)
    h.randomPopulate()

    return h

def run1(grid):
    grid.out()
    grid.plot()

def run2(grid):
    x = 5
    y = 5
    print(grid.neighborSum(x,y))

def run3(grid):
    #grid.out()
    grid.ising()
    grid.out()

def run4(grid):
    grid.isingNtimes(1000)

def runmp4(grid):
    N=2500
    T =100
    f=100
    grid.mp4ising(N,T,f)

def runMultMP4s(grid):
    grid.mp4wTs(500,tlist)

def makeFPlists(nList,fpn=[1000],secs=20):
    FPSlist = []
    FPNlist = []
    if len(fpn)==1:
        for n in nList:
            FPSlist.append(n/fpn[0]/secs)
            FPNlist.append(fpn[0])
        return FPSlist, FPNlist

    for i in range(len(nList)):
        FPSlist.append(nList[i]/fpn[i]/secs)
        FPNlist.append(fpn[i])

    return FPSlist, FPNlist


if __name__=='__main__':
    #h = setup()
    #h.plot()
    #run4(h)
    #h.plot()
    #runMultMP4s(h)
    #runmp4(h)

    parser = argparse.ArgumentParser()

    parser.add_argument('--iterations', '-I', nargs='+', type=int)
    parser.add_argument('--temp', '-T', nargs='+', type=float)
    parser.add_argument('--frames_per_second','-fps', type=int)
    parser.add_argument('--dimension','-D', nargs='+', type=int)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--frames_per_N', '-fpn', nargs='+',type=int)
    parser.add_argument('--seconds', '-secs', type=int)

    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)
        np.random.seed(args.seed)

    if args.iterations:
        N = args.iterations
    else:
        N = 2500

    if args.temp:
        tempList = args.temp
    else:
        tempList = [1]

    if args.frames_per_second:
        f = args.frames_per_second
    else:
        f = 1000

    if args.dimension:
        Xlist=args.dimension
    else:
        Xlist = [50]

    if args.frames_per_N:
        fpn = args.frames_per_N
    else:
        fpn=100

    if args.seconds:
        secs = args.seconds
    else:
        secs = 20

    FPSlist, FPNlist = makeFPlists(N,fpn,secs)

    print('Computation started at:',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mp4wTsXs(Xlist, tempList,N,FPSlist, FPNlist)
    print('Computation concluded at:',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    pass
