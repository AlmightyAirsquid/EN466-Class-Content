# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 16:13:23 2025

@author: logan
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

debug = 0

###Constants###

g=9.8
m=48/1000
Vi=70
p=1.29
A=0.0014
dt=0.1
secs=10

parser = argparse.ArgumentParser(description='Argument parser for golf.py')

parser.add_argument('--theta')

args=parser.parse_args()


###Drag Constants###

C=0.5

###Spin Constants###

sgm = 0.25

###Quality of Life Functions--Trajectory###

def makeVals(dt,secs):
    return secs/dt

vals = int(makeVals(dt,secs))


def eulerx(Vix,dt,vals):
    xVals = [0]
    for i in range(vals):
        xVals.append(xVals[i]+Vix*dt)
    if debug: print(xVals)
    return xVals

def eulerVy(Viy,dt,vals):
    VyVals = [Viy]
    for i in range(vals):
        VyVals.append(VyVals[i]-g*dt)
    if debug: print(VyVals)
    return VyVals

def eulery(Viy,dt,vals):
    yVals = [0]
    VyVals = eulerVy(Viy,dt,vals)
    for i in range(vals):
        if yVals[i] < 0: return yVals
        yVals.append(yVals[i]+VyVals[i]*dt)
    if debug: print(yVals)
    return yVals
        

###Trajectory Function###

def idealTraj(theta):
    Vix=Vi*math.cos(math.radians(theta))
    Viy=Vi*math.sin(math.radians(theta))
    
    xVals = eulerx(Vix,dt,vals)
    yVals = eulery(Viy,dt,vals)
    
    if debug: print(Vix,Viy)
    
    return [xVals,yVals]

def plotidealTraj(theta):
    trajVals = idealTraj(theta)
    
    yVals = trajVals[1]
    xVals = trajVals[0][0:len(yVals)]
    
    plt.plot(xVals,yVals)

#plotidealTraj(45)
#plotidealTraj(30)
#plt.show


###Quality of Life Functions--Drag###

##I didn't end up needing the following functions, but I might as well include their corpses##

#def dragVxEuler(Vi, Vix, A, m, dt, vals):
#    VxVals = [Vix]
#    for i in range(vals): 
#        VxVals.append(VxVals[i]-A/m*Vi*VxVals[i]*dt)
#    return VxVals

#def dragXEuler(Vi, Vix, A, m, dt, vals):
#    xVals = [0]
#    VxVals = dragVxEuler(Vi, Vix, A, m, dt, vals)
#    for i in range(vals):
#        xVals.append(xVals[i]+VxVals[i]*dt)
#    if debug: print(xVals)
#    return xVals

def dragVxyEuler(Vi, Vix, Viy, A, m, dt, C, vals):
    VyVals = [Viy]
    VxVals = [Vix]
    for i in range(vals):
        if (VyVals[i]**2+VxVals[i]**2)**0.5 < 14:
            VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VyVals[i]*dt)
            VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VxVals[i]*dt)
            #VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*dt)
            #VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*dt)
        else:
            VyVals.append(VyVals[i]-g*dt-7*p*A*VyVals[i]/m*dt)
            VxVals.append(VxVals[i]-7*p*A*VxVals[i]/m*dt)

    if debug: print(VxVals, VyVals)
    return [VxVals, VyVals]

def dragVxyEulerC1_2(Vi, Vix, Viy, A, m, dt, C, vals):
    VyVals = [Viy]
    VxVals = [Vix]
    for i in range(vals):
        VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VyVals[i]*dt)
        VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VxVals[i]*dt)
        #VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*dt)
        #VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*dt)
            
    if debug: print(VxVals, VyVals)
    return [VxVals, VyVals]


def dragXYEuler(Vi, Vix, Viy, A, m, dt, C, vals):
    yVals = [0]
    VyVals = dragVxyEuler(Vi, Vix, Viy, A, m, dt, C, vals)[1]
    xVals = [0]
    VxVals = dragVxyEuler(Vi, Vix, Viy, A, m, dt, C, vals)[0]
    for i in range(vals):
        if yVals[i] < 0: return [xVals, yVals]
        yVals.append(yVals[i]+VyVals[i]*dt)
        xVals.append(xVals[i]+VxVals[i]*dt)
    if debug: print(xVals, yVals)
    return [xVals, yVals]

def dragXYEulerC1_2(Vi, Vix, Viy, A, m, dt, C, vals):
    yVals = [0]
    VyVals = dragVxyEuler(Vi, Vix, Viy, A, m, dt, C, vals)[1]
    xVals = [0]
    VxVals = dragVxyEuler(Vi, Vix, Viy, A, m, dt, C, vals)[0]
    for i in range(vals):
        if yVals[i] < 0: return [xVals, yVals]
        yVals.append(yVals[i]+VyVals[i]*dt)
        xVals.append(xVals[i]+VxVals[i]*dt)
    if debug: print(xVals, yVals)
    return [xVals, yVals]


###Drag Trajectory Functions###

def dragTraj(theta):
    Vix=Vi*math.cos(math.radians(theta))
    Viy=Vi*math.sin(math.radians(theta))
    
    #xVals = dragXEuler(Vi, Vix, A, m, dt, vals)
    #yVals = dragYEuler(Vi, Viy, A, m, dt, vals)
    
    xVals = dragXYEuler(Vi, Vix, Viy, A, m, dt, C, vals)[0]
    yVals = dragXYEuler(Vi, Vix, Viy, A, m, dt, C, vals)[1]
    
    if debug: print(xVals,yVals)
    
    return [xVals, yVals]

def plotdragTraj(theta):
    trajVals = dragTraj(theta)
    
    if debug: print(trajVals)
    
    yVals = trajVals[1]
    xVals = trajVals[0][0:len(yVals)]
    
    plt.plot(xVals,yVals)
    

def dragTrajC1_2(theta):
    Vix=Vi*math.cos(math.radians(theta))
    Viy=Vi*math.sin(math.radians(theta))
    
    #xVals = dragXEuler(Vi, Vix, A, m, dt, vals)
    #yVals = dragYEuler(Vi, Viy, A, m, dt, vals)
    
    xVals = dragXYEulerC1_2(Vi, Vix, Viy, A, m, dt, C, vals)[0]
    yVals = dragXYEulerC1_2(Vi, Vix, Viy, A, m, dt, C, vals)[1]
    
    if debug: print(xVals,yVals)
    
    return [xVals, yVals]

def plotdragTrajC1_2(theta):
    trajVals = dragTrajC1_2(theta)
    
    if debug: print(trajVals)
    
    yVals = trajVals[1]
    xVals = trajVals[0][0:len(yVals)]
    
    plt.plot(xVals,yVals)


###Quality of Life Functions--Spin###


def spinEulerVyx(Vi, Vix ,Viy, A, m, dt, sgm, vals):
    VxVals = [Vix]
    VyVals = [Viy]
    for i in range(vals):
        if (VyVals[i]**2+VxVals[i]**2)**0.5 < 14:
            VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VyVals[i]*dt-sgm*VxVals[i]*dt)
            VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VxVals[i]*dt+sgm*VyVals[i]*dt)
            #VyVals.append(VyVals[i]-g*dt-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VyVals[i]*dt-sgm*dt)
            #VxVals.append(VxVals[i]-C*p*A*(VyVals[i]**2+VxVals[i]**2)**0.5/m*VxVals[i]*dt-sgm*dt)
        else:
            VyVals.append(VyVals[i]-g*dt-7*p*A*VyVals[i]*dt/m-sgm*VxVals[i]*dt)
            VxVals.append(VxVals[i]-7*p*A*VxVals[i]*dt/m+sgm*VyVals[i]*dt)
                
    return [VxVals, VyVals]

def spinXYEuler(Vi, Vix ,Viy, A, m, dt, sgm, vals):
    xVals = [0]
    yVals = [0]
    
    trajVals = spinEulerVyx(Vi, Vix, Viy, A, m, dt, sgm, vals)
    VxVals = trajVals[0]
    VyVals = trajVals[1]
    
    for i in range(vals):
        if yVals[i] < 0: return [xVals, yVals]
        xVals.append(xVals[i]+VxVals[i]*dt)
        yVals.append(yVals[i]+VyVals[i]*dt)
    return [xVals, yVals]

###Spin Trajectory Functions###

def spinTraj(theta):
    Vix=Vi*math.cos(math.radians(theta))
    Viy=Vi*math.sin(math.radians(theta))
    
    trajVals = spinXYEuler(Vi, Vix, Viy, A, m, dt, sgm, vals)
    xVals=trajVals[0]
    yVals=trajVals[1]
    
    if debug: print(xVals,yVals)

    return [xVals,yVals]

def plotspinTraj(theta):
    trajVals = spinTraj(theta)
    
    yVals = trajVals[1]
    xVals = trajVals[0][0:len(yVals)]
    
    plt.plot(xVals,yVals)

if args.theta:
    theta=float(args.theta)
else:
    theta=30

plotidealTraj(theta)
plotdragTrajC1_2(theta)
plotdragTraj(theta)
plotspinTraj(theta)
plt.savefig(f'golfPlotTheta{theta}.png')

