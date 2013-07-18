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
        #print max_z

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
    print distances
    print distances[0]

    #Separate surface &  bulk:
    surface = []
    surf_dist = []
    bulk = []
    bulk_dist = []
    for i in range(natoms):
        atom = atoms[i]
        z_diff = abs(float((atom[3] - max_z)))
       # print 'z_diff:',z_diff
        if z_diff <= width:
           surface.append(atom)
           surf_dist = np.concatenate((surf_dist,distances[i]),1)#The 1 means itll add arrays as rows
        if z_diff > width:
           bulk.append(atom)
           bulk_dist = np.concatenate((bulk_dist,distances[i]),1)
   # print'bulk=', bulk
    #print 'bulk_dis=',bulk_dist
    print surf_dist


    #Find bond lengths in bulk:
    SiSi_b = [] #Si-Si bond lengths for bulk
    SiO_b = []  #Si-O bond lengths for bulk
    OO_b = []   #O-O bond lengths for bulk
    for i in range(len(bulk)): #Loop through all the rows in dist_bulk
        bulk_atoms = bulk[i]

        if bulk_atoms[0] == 'Si':
           
            for j in range(natoms/3):#Loop through all the Si atoms of dist_bulk, go down the row
                if bulk_dist[i] > 0.0001 and bulk_dist[i] < 3.5: #Experiment says it is 3.06 A
                    SiSi_b.append(bulk_dist[i]) #Extracts all distance bewteen Si & Si that obey if

            for j in np.arange(natoms/3,natoms): #Loop through all the O atoms, going down the row
                if bulk_dist[i] > 0.0001 and bulk_dist[i] < 2: #Experiment says its 1.6A
                   SiO_b.append(bulk_dist[i]) # Extracts all distances b/w Si & O that obey if
    #print SiO_b
        #if bulk_atoms[0] == 'O':
    
            
                 
    average_SiSi_b = np.mean(SiSi_b)
    std_SiSi_b = np.std(SiSi_b,dtype = np.float64)
    print 'BULK: The average Si-Si bond length & standard deviation:',average_SiSi_b,std_SiSi_b

    #average_SiO_b = np.mean(SiO_b)
    #std_SiO_b = np.std(SiO_b,dtype = np.float64) 
    #print 'BULK: The average Si-O bond length & standard deviation:',average_SiO_b#,std_SiO_b



if __name__=='__main__':
     main()
