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
    
    #loops to find the distance between two atoms:
    for i in range(natoms): #loops over first atom
        atom1 = atoms[i] 

        for j in np.arange(i+1,natoms): #loops over a second atom,after i to avoid duplicate combos
            atom2 = atoms[j]
           # print 'atom1,atom2=', atom1,atom2  #test is good,produces (natoms choose 2) combos everytime    
          
            #Finds the difference between x,y,z coordinates of each pair
            x_pair_diff =float(atom1[0]) - float(atom2[0])
            y_pair_diff =float(atom1[1]) - float(atom2[1])
            z_pair_diff =float(atom1[2]) - float(atom2[2])        
           # print 'atom1[i],atom2[i],x_pair_diff=',atom1[2], atom2[2],z_pair_diff
            
            distances = (x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.)
           # print distances


# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
