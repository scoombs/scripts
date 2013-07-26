#!/usr/bin/env python

#Program reads in an SiO2 xyz file [for a PORE] & calculates number of nearest neighbours in surface Si,O & bulk Si,O atoms

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
        nsteps = int(sys.argv[4])
        radius = float(sys.argv[5])
     
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice first_gr_minimum nsteps radius (where these are floats,except nsteps=integer)\n'
        #Exit program cleanly
        sys.exit(0)

    #Allow user to input file name from terminal:
    filein = raw_input("Enter filename (xyz format):")
    inputfile = open(filein, 'r')
    
    
    distances = []
    for n in range(nsteps): #Time step loop

        natoms = int(inputfile.readline().strip()) #Reads in number of atoms
        #print natoms
        inputfile.readline() #Reads line2, blank space

        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
            atoms.append(line.split()) #Appends lists of atom coordinates [TYPE,x,y,z]
      
        #Convert elements to floats instead of strings: (Note: each 'row' is a set of coordinates for an atom: (TYPE,x,y,z))
        for row in atoms:
            for i in np.arange(1,len(row)):
                row[i] = float(row[i])

        #First find the centre of the pore:
         x_center = sum(row[1] for row in atoms)/natoms #Need to pick out the correct term, all the x's
         y_center = sum(row[2] for row in atoms)/natoms
         z_center = sum(row[3] for row in atoms)/natoms
         print x_center,y_center,z_center
       
       

        #To loop over only all pairs of atoms:
        for i in range(natoms):
            atom1 = atoms[i]

            for j in range(natoms):#Loops over second atom,doesn't account for duplicates
                atom2 = atoms[j]
          
                #Finds the difference between x,y,z coordinates of each pair:
                x_pair_diff = float(atom1[1]) - float(atom2[1])
                y_pair_diff = float(atom1[2]) - float(atom2[2])
                z_pair_diff = float(atom1[3]) - float(atom2[3])
            
                #Need to consider affects of periodic boundary conditions:
                x_pair_diff -= lattice_x*pbc_round(x_pair_diff/lattice_x)
                y_pair_diff -= lattice_y*pbc_round(y_pair_diff/lattice_y)
                z_pair_diff -= lattice_z*pbc_round(z_pair_diff/lattice_z)
   
                distances.append((x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.))
    distances = scipy.array(distances) #Creates scipy array
    distances = scipy.reshape(distances,(nsteps*natoms,-1))
   # print distances

    #Separate surface & bulk surrounding pore,captures indices for atoms that obey statements
    surface = []
    bulk = []
    for i in range(len(atoms)):
        z_diff = abs(float((atoms[i][3] - max_z)))
        if z_diff <= width:
            surface.append(i) #This gives COLUMN indices for surface atoms
        else:
            bulk.append(i)
   # print'bulk=', bulk
   # print 'surf = ',surface,len(surface),natoms
    
 

if __name__=='__main__':
     main()
