#!/usr/bin/env python
#Computes pair correlation function,g(r),taking *.xyz input file
import os,sys
import numpy as np 

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
    for i in range(natoms): #loops over first atom
        atom1 = atoms[i] 
        #print 'atom1 =',atom1
        for j in np.arange(i,natoms): #loops over a second atom,after i to avoid duplicate combos
            atom2 = atoms[j]
          #  print 'atom2 =' ,atom2 
            if atom1 != atom2: #create a pair of all possible combos of 2 different atoms
             #  print atom1,atom2     
               pairs.append([atom1,atom2]) #stores pairs in a list called "pairs"
               print pairs        

# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
