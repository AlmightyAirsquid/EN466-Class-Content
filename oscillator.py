# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 18:28:32 2025

@author: logan
"""

import math
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument('--RUN')

args = parser.parse_args()

g = 9.8
l = 9.8
gamma = 0.25
alpha = 0.5
#omega = 1

def calc2ndDerivative(t, theta, thetaPrime, omega=0.666):
    return -1*g/l*theta-2*gamma*thetaPrime+alpha*math.sin(omega*t)

def calc2ndDerivativeNoSin(t, theta, thetaPrime, omega=1):
    return -1*g/l*theta-2*gamma*thetaPrime+alpha*omega*t

def euler(val, valPrime, dt):
    return val+dt*valPrime

def euler2x(valList1, valList2, dt):
    return euler(valList1[0], valList1[1], dt), euler(valList2[0], valList2[1], dt)

def rk4(t, theta, thetaPrime, dt, omega=1):
    
    k1theta = thetaPrime
    k1thetaPrime = calc2ndDerivative(t, theta, thetaPrime)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k1theta], 
        [thetaPrime, k1thetaPrime], 
        dt/2
        )
    
    k2theta = thetaPrimeTemp
    k2thetaPrime = calc2ndDerivative(t+dt/2, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k2theta], 
        [thetaPrime, k2thetaPrime], 
        dt/2
        )
    
    k3theta = thetaPrimeTemp
    k3thetaPrime = calc2ndDerivative(t+dt/2, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k3theta], 
        [thetaPrime, k3thetaPrime], 
        dt
        )
    
    k4theta = thetaPrimeTemp
    k4thetaPrime = calc2ndDerivative(t+dt, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k4theta], 
        [thetaPrime, k4thetaPrime], 
        dt
        )
    
    thetaNew = theta + dt/6*(k1theta+2*k2theta+2*k3theta+k4theta)
    thetaPrimeNew = thetaPrime + dt/6*(k1thetaPrime+2*k2thetaPrime+2*k3thetaPrime+k4thetaPrime)
    tNew = t + dt
    
    return tNew, thetaNew, thetaPrimeNew

def rk4NoSin(t, theta, thetaPrime, dt, omega=1):
    
    k1theta = thetaPrime
    k1thetaPrime = calc2ndDerivativeNoSin(t, theta, thetaPrime)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k1theta], 
        [thetaPrime, k1thetaPrime], 
        dt/2
        )
    
    k2theta = thetaPrimeTemp
    k2thetaPrime = calc2ndDerivativeNoSin(t+dt/2, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k2theta], 
        [thetaPrime, k2thetaPrime], 
        dt/2
        )
    
    k3theta = thetaPrimeTemp
    k3thetaPrime = calc2ndDerivativeNoSin(t+dt/2, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k3theta], 
        [thetaPrime, k3thetaPrime], 
        dt
        )
    
    k4theta = thetaPrimeTemp
    k4thetaPrime = calc2ndDerivativeNoSin(t+dt, thetaTemp, thetaPrimeTemp, omega)
    
    thetaTemp, thetaPrimeTemp = euler2x(
        [theta, k4theta], 
        [thetaPrime, k4thetaPrime], 
        dt
        )
    
    thetaNew = theta + dt/6*(k1theta+2*k2theta+2*k3theta+k4theta)
    thetaPrimeNew = thetaPrime + dt/6*(k1thetaPrime+2*k2thetaPrime+2*k3thetaPrime+k4thetaPrime)
    tNew = t + dt
    
    return tNew, thetaNew, thetaPrimeNew


def makeValLists(xStop, dt, iTheta, iThetaPrime, omega=1, xStart=0):
    
    numSteps = int((xStop-xStart)/dt)
    
    t = xStart 
    tList = [t]
    
    theta = iTheta
    thetaList = [theta]
    
    thetaPrime = iThetaPrime
    thetaPrimeList = [thetaPrime]
    
    for i in range(numSteps):
        t, theta, thetaPrime = rk4(t, theta, thetaPrime, dt, omega)
        
        tList.append(t)
        thetaList.append(theta)
        thetaPrimeList.append(thetaPrime)
        
    return [tList, thetaList, thetaPrimeList]

def makeValListsNoSin(xStop, dt, iTheta, iThetaPrime, omega=1, xStart=0):
    
    numSteps = int((xStop-xStart)/dt)
    
    t = xStart 
    tList = [t]
    
    theta = iTheta
    thetaList = [theta]
    
    thetaPrime = iThetaPrime
    thetaPrimeList = [thetaPrime]
    
    for i in range(numSteps):
        t, theta, thetaPrime = rk4NoSin(t, theta, thetaPrime, dt, omega)
        
        tList.append(t)
        thetaList.append(theta)
        thetaPrimeList.append(thetaPrime)
        
    return [tList, thetaList, thetaPrimeList]

def plotFunction(xStop, dt, iTheta, iThetaPrime, omega=1, pT=True, pTP=True):
    
    valLists = makeValLists(xStop, dt, iTheta, iThetaPrime, omega)
    
    if pT: plt.plot(valLists[0], valLists[1], label=f'Initial theta: {round(iTheta, 3)}\n omega={omega}')
    if pTP: plt.plot(valLists[0], valLists[2], label=f"initial theta': {round(iThetaPrime)}\n omega={omega}")
    
    plt.xlabel('t (seconds)')
    plt.ylabel('Theta (rad)')
    plt.title(f'Function of theta versus time')
    
def plotFunctionNoSin(xStop, dt, iTheta, iThetaPrime, omega=1, pT=True, pTP=True):
    
    valLists = makeValListsNoSin(xStop, dt, iTheta, iThetaPrime, omega)
    
    if pT: plt.plot(valLists[0], valLists[1], label=f'Initial theta: {round(iTheta, 3)}\n omega={omega}')
    if pTP: plt.plot(valLists[0], valLists[2], label=f"initial theta': {round(iThetaPrime)}\n omega={omega}")
    
    plt.xlabel('t (seconds)')
    plt.ylabel('Theta (rad)')
    plt.title(f'Function of theta versus time (alpha 1.2)')
    
def plotFunctionsofOmega(iTheta, iThetaPrime, *omegas, xStop=25, dt=0.01, plotTheta=True, plotThetaPrime=True, saveplot=False):
    pT = plotTheta
    pTP = plotThetaPrime
    for omega in omegas:
        plotFunction(xStop, dt, math.radians(iTheta), iThetaPrime, omega, pT, pTP)
        if saveplot:
            plt.show()
            plt.legend()
            if iThetaPrime < 0:
                iThetaPrimeText = f'n{int(abs(iThetaPrime))}'
            else:
                iThetaPrimeText = f'{int(abs(iThetaPrime))}'
                
            omegaText = str(omega)
            omegaText = omegaText.split('.')
            omegaText = 'p'.join(omegaText)
                
            plt.savefig(f'plottedFunctionsofOmega_iTheta{iTheta}_iThetaPrime{iThetaPrimeText}_omega{omegaText}.png')
            
            plt.close()
            
    plt.legend()
    
def plotFunctionofOmegaNoSin(iTheta, iThetaPrime, *omegas, xStop=25, dt=0.01, plotTheta=True, plotThetaPrime=True, saveplot=False):
    pT = plotTheta
    pTP = plotThetaPrime
    for omega in omegas:
        plotFunctionNoSin(xStop, dt, math.radians(iTheta), iThetaPrime, omega, pT, pTP)
        if saveplot:
            plt.show()
            plt.legend()
            if iThetaPrime < 0:
                iThetaPrimeText = f'n{int(abs(iThetaPrime))}'
            else:
                iThetaPrimeText = f'{int(abs(iThetaPrime))}'
                
            omegaText = str(omega)
            omegaText = omegaText.split('.')
            omegaText = 'p'.join(omegaText)
                
            plt.savefig(f'Alpha1p2_plottedFunctionsofOmegaNoSin_iTheta{iTheta}_iThetaPrime{iThetaPrimeText}_omega{omegaText}.png')
            
            plt.close()
            
    plt.legend()
    
    
def plotFunctionsofDeltaTheta(omega, iThetaPrime, *iThetas, xStop=25, dt=0.01, plotTheta=True, plotThetaPrime=True, saveplot=False):
    pT = plotTheta
    pTP = plotThetaPrime
    for iTheta in iThetas:
        plotFunction(xStop, dt, math.radians(iTheta), iThetaPrime, omega, pT, pTP)
        if saveplot:
            plt.show()
            plt.legend()
            if iThetaPrime < 0:
                iThetaPrimeText = f'n{int(abs(iThetaPrime))}'
            else:
                iThetaPrimeText = f'{int(abs(iThetaPrime))}'
                
            omegaText = str(omega)
            omegaText = omegaText.split('.')
            omegaText = 'p'.join(omegaText)
                
            plt.savefig(f'iThetaVarried_Alpha1p2_plottedFunctionsofOmegaNoSin_iThetaPrime{iThetaPrimeText}_omega{omegaText}.png')
            
            plt.close()
            
    plt.legend()
    

def run1():
    
    plotFunction(100, 0.01, math.radians(40), -5, 3)
    
def run2():
    
    plotFunctionsofOmega(90, -1, .2, .4, .6, .8, 1, 1.2, 1.4, 1.6, 1.8, 2, saveplot=True)
    
def run4():
    plotFunctionofOmegaNoSin(90, -1, .2, .4, .6, .8, 1, 1.2, 1.4, 1.6, 1.8, 2, saveplot=True)

def run5():
    plotFunctionsofDeltaTheta(0.666, -1, 89.9, 89.95, 90, 90.05, 90.1, xStop=40, saveplot=False)

if __name__=='__main__':
    
    #run1()
    run5()
    pass

if args.RUN:
    
    if args.RUN==1:
        print('run not applicble')
        pass
    
    if args.RUN==2:
        
        run1()
        
        pass
    
    if args.RUN==3:
        run2()
        pass
    
    if args.RUN==4:
        run4()
        pass
    
    if args.RUN==5:
        run5()
        pass
