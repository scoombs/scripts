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
 
    inputfile = open('test.xyz','r')
    outputfile = open('test_hole.xyz','w')
   
    natoms = inputfile.readline().strip() #Reads in number of atoms
    inputfile.readline() #Skips line 2 (blank/comment line)
    
    




if __name__=='__main__':
    main() 
