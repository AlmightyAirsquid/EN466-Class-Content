import sys
import argparse as ap 
import matplotlib.pyplot as plt
import numpy as np
import math
        

xSpace = np.linspace(-10,10,401)

#print(xSpace)

def sinc(x):
    if x==0: return 1
    return math.sin(x)/x

def genFunction(funIn):
    ySpace = []
    if funIn == 'cos':
        for i in range(len(xSpace)):
            ySpace.append(math.cos(xSpace[i]))
    elif funIn == 'sin':
        for i in range(len(xSpace)):
            ySpace.append(math.sin(xSpace[i]))
    elif funIn == 'sinc':
        for i in range(len(xSpace)):
            ySpace.append(sinc(xSpace[i]))
    else:
        for i in range(len(xSpace)):
            ySpace.append(0)
        print('Warning: {funIn} is not in function library. Plotting line y=0 instead.')
        return ySpace
    return ySpace



title = []
width = 6



#plt.plot(xSpace,ySpace)
#plt.title("Trigenometry Function Output")
#plt.show()

#plt.savefig('sine_wave.pdf')


if __name__ == "__main__":
    parser = ap.ArgumentParser(prog='trigonometry', description='Accepts arguments for trigonometry.py.')
#Longhands
    parser.add_argument('-f', '--function', type=str, help='Function to be plotted (sin, cos, sinc... etc).')
    parser.add_argument('-w', '--write', type=str, help='Writes an ASCII file with a table.')
    parser.add_argument('-r', '--read_from_file', type=str, help='Reads ASCII file and produces plot accordingly.')
    parser.add_argument('-p', '--print', type=str, help='Choose the format which the file will be saved as.')
    args = parser.parse_args()
    
    if args.write:
        tabData = [xSpace]
        
        funList = args.function.split(',')
        for i in range(len(funList)):
            tabData.append(genFunction(funList[i]))
        
        #for i in tabData:
            #print(i)
            #print('\n')
        
        with open(f'{args.write}','w') as f:
            
            f.write('|')
            f.write(f'{"x":^{width}}')
            f.write('|')

            for i in list(args.function.split(',')):
                f.write(f'{i:^{width}}')
                f.write('|')
                
            f.write('\n')
            
            for j in range(len(tabData[0])):
                f.write('|')
                for i in range(len(tabData)):
                    if (tabData[i][j] < 0 and tabData[i][j] > -10) or tabData[i][j] >= 10:
                        f.write(f'{tabData[i][j]:.2f} |')
                    elif tabData[i][j] <=-10:
                        f.write(f'{tabData[i][j]:.2f}|')
                    else:
                        f.write(f' {tabData[i][j]:0.2f} |')
                f.write('\n')
            pass
            
    if args.read_from_file:
        
        with open(f'{args.read_from_file}','r') as f:
            
            fileText = f.read()
            
            splitText = fileText.split('\n')

            #print(splitText)

            fullList1 = []
            fullList2 = []
            fullList3 = []

            for i in range(len(splitText)):
                fullList1.append(splitText[i].split('|'))

            #print(fullList1)

            title = fullList1.pop(0)[1:-1]

            #print(title)

            #print(fullList1)


            for i in range(len(fullList1)-1):
                fullList2.append(fullList1[i][1:-1])



            for i in range(len(fullList2)):
                for j in range(len(fullList2[i])):
                    fullList2[i][j] = float(fullList2[i][j])
                
            ###Make the Plot

            for j in range(len(fullList2[0])):
                
                tempList = []
                
                for i in range(len(fullList2)):
                    
                    tempList.append(fullList2[i][j])

                fullList3.append(tempList)
                    
            for i in range(len(fullList3[1::])):
                plt.plot(xSpace, fullList3[i+1], label=title[i+1])
            
            tempTitle = 'Plot of '
            
            
            if len(title) >2:
                for i in range(len(title[1::])):
                    tempTitle += title[i+1]
                    title += ' '
            else:
                tempTitle += f'{title[-1]}'
            
            plt.title(tempTitle)
            plt.legend()
            
            
        
        pass
    
    if args.function:
        funList = args.function.split(',')
        for i in funList:
            plt.plot(xSpace,genFunction(i), label=i)
            title.append(i)
        tempTitle = 'Plot of '
        if len(title) >1:
            for item in title:
                tempTitle += str(item)
            pass
        else:
            tempTitle += str(title)
            pass
        plt.title(str(tempTitle))
        #print(title)
        #print('--function executed successfully')
        plt.legend()
        
        
    if args.print:
        
        plt.savefig(f'{args.print}')
