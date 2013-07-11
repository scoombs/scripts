#!/usr/bin/env python

#Program used to calculate differnt properties about atom's nearest neighbours

import os,sys
import numpy as np
import scipy
def pbc_round(input_value):
    """
This function is used for periodic boundary conditions,it rounds a value to the nearest integer.

"""
    i = int(input_value)
    if (abs(input_value-i) >= 0.5):
        if (input_value > 0): i+=1
        if (input_value < 0): i-=1
    return i 

def main():
    
     #Allow the user to input the periodic boundary conditions (box size) and number of timesteps to be used:
    try:
        program =sys.argv[0] #Gives filename
        lattice = float(sys.argv[1])
        lattice_x = lattice#float(sys.argv[2])
        lattice_y = lattice#float(sys.argv[3])
        lattice_z = float(sys.argv[2])
        first_minimum = float(sys.argv[3])
       # nsteps = int(sys.argv[2])
     
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice first_gr_minimum nsteps (where lattice & nsteps & nbins are floats)\n'
        #Exit program cleanly
        sys.exit(0)

    inputfile = open('TEST.xyz','r')
    outputfile = open('nn.dat','w')
    
    distances = []
   
    for n in range(1): #Time step loop

        natoms = int(inputfile.readline().strip()) #Reads in number of atoms 
        inputfile.readline() #Reads line2, blank space

        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
            atoms.append(line.split()) #Appends lists of atom coordinates [TYPE,x,y,z]
       
       # atoms = scipy.array(atoms) #Creates an n-d array 
       # print atoms
        
        #Loops to find the distance between two atoms:
        for i in range(natoms): #Loops over first atom
            atom1 = atoms[i]
                                        
            for j in range(natoms):#Loops over second atom,doesn't account for duplicates
                atom2 = atoms[j]
               # print 'atom1,atom2=', atom1,atom2 
          
                #Finds the difference between x,y,z coordinates of each pair:
                x_pair_diff = float(atom1[1]) - float(atom2[1])
                y_pair_diff = float(atom1[2]) - float(atom2[2])
                z_pair_diff = float(atom1[3]) - float(atom2[3])
               # print 'atom1[i],atom2[i],x_pair_diff=',atom1[2], atom2[2],z_pair_diff
            
                #Need to consider affects of periodic boundary conditions:
                x_pair_diff -= lattice_x*pbc_round(x_pair_diff/lattice_x)
                y_pair_diff -= lattice_y*pbc_round(y_pair_diff/lattice_y)
                z_pair_diff -= lattice_z*pbc_round(z_pair_diff/lattice_z)
               # print x_pair_diff
                distances.append((x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.))
        distances = scipy.array(distances) #Creates scipy array
        distances = scipy.reshape(distances,(natoms,-1)) #Unspecified value should assume to be natoms as well 
        #Distances is square,symmetric matrix 
        print distances
    #Loop through the distance matrix & determine number of nearest neighbours per atom
    nn = [] #nearest neighbours array
    tmp = []
    for i in range(natoms):#loop through rows
        for j in np.arange(natoms):#loop through each element in row
            if distances[i,j] > 0.0001 and distances[i,j] < first_minimum:  #first minima of the g(r) function
                nn.append(distances[i,j])
                tmp = len(nn)
                
                
        print nn,tmp

   

if __name__=='__main__':
     main()
