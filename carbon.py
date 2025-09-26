import math
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Argument parser for carbon.py')

parser.add_argument('--plot')

args=parser.parse_args()

tao=8223
N0 = 10**(-9)*6.022*10**(23)

def euler(N0,stepsize,years):
    numList =[N0]
    steps=int(years/stepsize)
    for i in range(steps):
        numList.append(numList[i]-1/tao*numList[i]*stepsize)
    return numList

def makexSpace(stepsize,years):
    steps = int(years/stepsize)
    return np.linspace(0, years,steps+1)

#print(euler(N0,100,20000))
years=20000

def plotEQ(stepsize,years):
    plt.plot(makexSpace(stepsize,years),euler(N0,stepsize,years))
    pass

def pdiffatxyears(stepsize1,stepsize2,year):
    v1=euler(N0,stepsize1,year)[-1]
    v2 = euler(N0,stepsize2,year)[-1]
    return 2*abs(v1-v2)/(v1+v2)*100

def realpdiff(stepsize,year):
    v1=euler(N0,stepsize,year)[-1]
    v2=N0*math.e**(-year/tao)
    return 2*abs(v1-v2)/(v1+v2)*100

#print(f'Relative difference between step size of 100 and 1000 is {pdiffatxyears(100, 1000, 5700*2):.2f}'+'%')
#print(f'Relative difference between step size of 10 and 100 is {pdiffatxyears(10, 100, 5700*2):.2f}'+'%')
#print(f'Asolute difference between real value and step size of 100 is {realpdiff(100,5700*2):.2f}'+'%')
#plotEQ(100,years)
#plotEQ(10,years)
#plotEQ(1000,years)
#plotEQ(5000,years)

if args.plot:
    stepsize=args.plot
    plotEQ(stepsize,years)
else:
    stepsize=100

#plt.show()
plt.savefig(f'carbonWidth{stepsize}.png')
