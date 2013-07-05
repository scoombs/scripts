#!/usr/bin/env python
#This program reads in an xyz file & removes a hole out of the centre with radius specified by user in nm
import os,sys
import numpy as np
def main():
    
    #Allow user input of hole radius:
    try:
        program = sys.argv[0] #Gives filename
        radius = float(sys.argv[1])
    except IndexError:
        #Tell user what is needed
        print '\n usage: '+program+' radius (where radius of the hole is a float)'
        sys.exit(0)
 
    inputfile = open('test0.xyz','r')
    outputfile = open('test_hole.xyz','w')
   
    natoms = int(inputfile.readline().strip()) #Reads in number of atoms
    #print natoms,type(natoms)
    inputfile.readline() #Skips line 2 (blank/comment line)
    
    #First need to find the centre of the bulk given
    x = []
    y = []
    z = []
    for i in range(natoms):
        line = inputfile.readline()
        x.append(float(line.split()[1]))
        y.append(float(line.split()[2]))
        z.append(float(line.split()[3]))
    print x,y,z
    inputfile.close()
        
    




if __name__=='__main__':
    main() 
