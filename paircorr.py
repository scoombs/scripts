#!/usr/bin/env python
#Computes pair correlation function,g(r),taking *.xyz input file
import os,sys
import numpy as np 

def main():
    """
    This is the main function.
    """
    #Allow the user to input a lattice constant and number of bins to be used:
    try:
        program =sys.argv[0] #Gives filename
        lattice = int(sys.argv[1])
        nbins = int(sys.argv[2])
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice nbins (where lattice & nbins are integers)\n' 
        #Exit program cleanly
        sys.exit(0)

    inputfile = open( 'test.xyz' , 'r')
    outfile = open('paircorr_data' , 'w')
   
    natoms = int(inputfile.readline().split()[0])  #Reads line 1,number of atoms
    inputfile.readline() #Reads line 2, blank space
  
    atoms = []
    for line in inputfile:
#        x= line.split()[1]
#        y= line.split()[2]
#        z= line.split()[3]
#        lists.append([x,y,z])

        tmp = line.split() # Splits list
        tmp.pop(0)         # Pops off first entry in each list (atom type)
        atoms.append(tmp)  # Appends lists of atom coordinates together
    
    #Loops to find the distance between two atoms:
    for i in range(natoms): #Loops over first atom
        atom1 = atoms[i] 

        for j in np.arange(i+1,natoms): #Loops over a second atom,after i to avoid duplicate combos
            atom2 = atoms[j]
           # print 'atom1,atom2=', atom1,atom2  #Test is good,produces (natoms choose 2) combos everytime    
          
            #Finds the difference between x,y,z coordinates of each pair:
            x_pair_diff =float(atom1[0]) - float(atom2[0])
            y_pair_diff =float(atom1[1]) - float(atom2[1])
            z_pair_diff =float(atom1[2]) - float(atom2[2])        
           # print 'atom1[i],atom2[i],x_pair_diff=',atom1[2], atom2[2],z_pair_diff
            
            distances = (x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.)
           # print distances

            hist,bin_edges = np.histogram(distances,bins=nbins, range=(0,lattice/2))
            print hist,bin_edges
# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
