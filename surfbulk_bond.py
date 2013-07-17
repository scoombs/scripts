#!/usr/bin/env python
#Program reads in an xyz file & calculates bond lengths, Si-O Si-Si,O-O

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
        width = float(sys.argv[3])
        nsteps = int(sys.argv[4])
     
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice width(A) nsteps (all are floats,except nsteps is an integer)\n'
        #Exit program cleanly
        sys.exit(0)

   #Allow user to input file name from terminal:
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

         #Convert elements to floats instead of strings: (Note: each 'row' is a set of coordinates for an atom: (TYPE,x,y,z))
        for row in atoms:
            for i in np.arange(1,len(row)):
                row[i] = float(row[i])

        #First find the maximum z value:
        z = []
        for i in range(natoms):
            atom = atoms[i]
            z.append(float(atom[3]))
        max_z = max(z)
        print max_z

        #Loops to find the distance between any two atoms
        for i in range(natoms): #Loops over first atom in the atom pairs
            atom1 = atoms[i]
           # print atom1     
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
    distances = scipy.reshape(distances,(nsteps*natoms,-1))#Reshapes array into a square matrix,undeclared should be natoms as well
   # print distances

    #Separate surface &  bulk:
    surface = []
    surf_dist = []
    bulk = []
    bulk_dist = []
    for i in range(natoms):
        atom = atoms[i]
        z_diff = abs(float((atom[3] - max_z)))
        if z_diff <= width:
           surface.append(atom)
           surf_dist.append(distances[i,j])
   # print surface
   # print surf_dist
        if z_diff > width:
           bulk.append(atom)
           bulk_dist.append(distances[i,j])
   # print bulk
   # print bulk_dist
    
    
    #Loop through to find Si-O bond lengths:
    SiO = []
    for i in range(natoms/3): #Si are the first 3rd of atoms in xyz file (since we have SiO2)
        for j in np.arange(natoms/3,natoms):#Looks at O distances
            if distances[i,j] > 0.0001 and distances[i,j] < 2: #Experiment says it is 1.6 A, so I chose 2 A
                SiO.append(distances[i,j]) #Extracts all distance bewteen Si & Si that obey if
               
    average_SiO = np.mean(SiO)
    print 'The average Si-O bondlength is:',average_SiO
    std_SiO = np.std(SiO,dtype = np.float64)
    print 'The standard deviation (Si-O) is:',std_SiO
       
    #Loop through to find Si-Si bond lengths:
    SiSi = []
    for i in range(natoms/3):
        for j in range(natoms/3):
            if distances[i,j] > 0.0001 and distances[i,j] < 3.5: #Experiment says it is 3.06
                SiSi.append(distances[i,j])
    average_SiSi = np.mean(SiSi)
    print 'The average Si-Si bondlength is:',average_SiSi
    std_SiSi = np.std(SiSi,dtype = np.float64)
    print 'The standard deviation (Si-Si) is:',std_SiSi

    #Loop through to find O-O bond lengths:
    OO = []
    for i in np.arange(natoms/3,natoms):
        for j in np.arange(natoms/3,natoms):
            if distances[i,j] > 0.0001 and distances[i,j] < 3: #Experiment says it is 2.6
                OO.append(distances[i,j])
    average_OO = np.mean(OO)
    print 'The average O-O bondlength is:',average_OO
    std_OO = np.std(OO,dtype = np.float64)
    print 'The standard deviation (O-O) is:',std_OO

if __name__=='__main__':
     main()
