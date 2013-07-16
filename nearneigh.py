#!/usr/bin/env python

#Program used to calculate differnt properties about atom's nearest neighbours
#There is an option to calculate # nn for Si or O, need to uncomment & comment approporiate loops,described below
#Look at the 3 areas in the code with **************** for further help

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
     
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice first_gr_minimum nsteps (where lattice & nsteps & nbins are floats)\n'
        #Exit program cleanly
        sys.exit(0)

   #Allow user to input file name from terminal:
    print 'NOTE:Please see script for changes needed depending on wanting Si or O nearest neighbour claculations.'
    filein = raw_input("Enter filename (xyz format):")
    inputfile = open(filein, 'r')
    
    
    distances = []
    for n in range(nsteps): #Time step loop

        natoms = int(inputfile.readline().strip()) #Reads in number of atoms 
        inputfile.readline() #Reads line2, blank space

        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
            atoms.append(line.split()) #Appends lists of atom coordinates [TYPE,x,y,z]
        
        #Loops to find the distance between any two atoms(this is the general form, to specify atom type comment this loop out&see below)
       # for i in range(natoms): #Loops over first atom in the atom pairs
           # atom1 = atoms[i]

        #*****Change loop to go over a specific first atom or type:*****

        #To loop over only **O** uncomment:
        #for i in np.arange(natoms/3,natoms): 
           # atom1 = atoms[i] 

        #To loop over only **Si** instead just uncomment : 
        for i in range(natoms/3):
            atom1 = atoms[i]
        #*****************************************************************
                                
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
    
    #**********************************
   #distances = scipy.reshape(distances,(nsteps*natoms,-1))

    #IF chose above to only calculate ***O*** nn,must uncomment this instead:
    #distances = scipy.reshape(distances,(nsteps*natoms*2/3,-1)) 

    #IF chose above to only calcuate ***Si*** nn must uncomment this instead:
    distances = scipy.reshape(distances,(nsteps*natoms/3,-1))

    #Unspecified value should assume to be natoms  
    #***********************************

    #Loop through the distance matrix & determine number of nearest neighbours per atom
    nn = [] #Nearest neighbours count array
    tmp = [] #Temporary array for nn distance storage
    
    #**********************************************
    for i in range(nsteps*natoms/3):
    # Change above range to range(nsteps*natoms*2/3) for just ***O*** OR range(nsteps*natoms/3) for just ***Si***
    #***********************************************

        for j in np.arange(natoms):#Loop through each element in row
            if distances[i,j] > 0.0001 and distances[i,j] < first_minimum:  #First minima of the g(r) function
                tmp.append(distances[i,j]) #Extracts all distance in col. i that obey if statement
                row_nn = len(tmp) #Determines the number of distances obeying if
        tmp[:] = [] #Clears tmp before moving to the next row
        nn.append(row_nn)#Creates an array with each row representing the count of nn for each atom1
    
    
    #Find the average number of nearest neighbours:
    average_nn = np.mean(nn)
    print 'The average number of nearest neighbours is:',average_nn
    #Find the standard deviation: std = sqrt(mean(abs(x - x.mean())**2))
    std_dev = np.std(nn,dtype = np.float64)
    print 'The standard deviation is:',std_dev
    

if __name__=='__main__':
     main()
