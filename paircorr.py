#!/usr/bin/env python
#Computes pair correlation function,g(r),taking *.xyz input file
import os,sys
import numpy as np
import sets

def main():
    """
    This is the main function.
    """
    inputfile = open( 'test.xyz' , 'r')
    outfile = open('paircorr_data' , 'w')
    
    natoms = int(inputfile.readline().split()[0])  #reads line 1,number of atoms
    inputfile.readline() # reads line 2, blank space
  
    atoms = []
    for line in inputfile:
#        x= line.split()[1]
#        y= line.split()[2]
#        z= line.split()[3]
#        lists.append([x,y,z])

        tmp = line.split() # splits list
        tmp.pop(0)         # pops off first entry in each list (atom type)
        atoms.append(tmp)  # appends lists of atom coordinates together
    
    #loop to find the distance between two atoms
    pairs = []
    for atom1 in atoms:
        print 'atom1 =',atom1
        for atom2 in atoms:
            if atom1 != atom2:     
               pairs.append([atom1,atom2])
               pair = set(tuple(pairs))
               print pair 

# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
