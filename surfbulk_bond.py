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
    #print distances
    
    #Separate surface & bulk,captures indices for atoms that obey statements
    surface = []
    bulk = []
    for i in range(len(atoms)):
        z_diff = abs(float((atoms[i][3] - max_z)))
        if z_diff <= width:
            surface.append(i)
        else:
            bulk.append(i)
    #print'bulk=', bulk
    #print 'surf = ',surface

    #Find bond lengths in surface:
    SiSi_surf = [] #Si-Si bond lengths for surface
    SiO_surf = []  #Si-O bond lengths for surface
    OO_surf = []   #O-O bond lengths for surface
    for i in surface: #Loop through all the indices elements for location of atoms on surface in atoms list 

        if atoms[i][0] == 'Si':
           
            for j in range(natoms/3):#Loop through all the Si atoms in surface
                if distances[i,j] > 0.0001 and distances[i,j] < 3.5: #Experiment says it is 3.06 A
                    SiSi_surf.append(distances[i,j]) #Extracts all distance bewteen Si & Si that obey if

            for j in np.arange(natoms/3,natoms): #Loop through all the O atoms, going down the row
                if distances[i,j] > 0.0001 and distances[i,j] < 2: #Experiment says its 1.6A
                   SiO_surf.append(distances[i,j]) # Extracts all distances b/w Si & O that obey if
    
        if atoms[i][0] == 'O':
       
            for j in np.arange(natoms/3,natoms): #Loops through all O atoms, going down the row
                if distances[i,j] > 0.0001 and distances[i,j] < 3: #Experiment says its 2.6
                 OO_surf.append(distances[i,j]) #Extracts distances b/w O-O obeying if
  
    average_SiSi_surf = np.mean(SiSi_surf)
    std_SiSi_surf = np.std(SiSi_surf,dtype = np.float64)
    print 'SURFACE: The average Si-Si bond length & standard deviation:',average_SiSi_surf,std_SiSi_surf

    average_SiO_surf = np.mean(SiO_surf)
    std_SiO_surf = np.std(SiO_surf,dtype = np.float64) 
    print 'SURFACE: The average Si-O bond length & standard deviation:',average_SiO_surf,std_SiO_surf

    average_OO_surf = np.mean(OO_surf)
    std_OO_surf = np.std(OO_surf,dtype = np.float64)
    print 'SURFACE: The average O-O bond length & standard deviation:', average_OO_surf,std_SiO_surf
  
    #Find bond lengths in bulk:
    SiSi_bulk = [] #Si-Si bond lengths for bulk
    SiO_bulk = [] #Si-O bond lengths for bulk
    OO_bulk = [] #O-O bond lengths for bulk
    for i in bulk: #Loop through all the indices elements for location of atoms on surface in atoms list

        if atoms[i][0] == 'Si':
           
            for j in range(natoms/3):#Loop through all the Si atoms of bulk
                if distances[i,j] > 0.0001 and distances[i,j] < 3.5: #Experiment says it is 3.06 A
                    SiSi_bulk.append(distances[i,j]) #Extracts all distance bewteen Si & Si that obey if

            for j in np.arange(natoms/3,natoms): #Loop through all the O atoms, going down the row
                if distances[i,j] > 0.0001 and distances[i,j] < 2: #Experiment says its 1.6A
                   SiO_bulk.append(distances[i,j]) # Extracts all distances b/w Si & O that obey if
    
        if atoms[i][0] == 'O':
       
            for j in np.arange(natoms/3,natoms): #Loops through all O atoms, going down the row
                if distances[i,j] > 0.0001 and distances[i,j] < 3: #Experiment says its 2.6
                 OO_bulk.append(distances[i,j]) #Extracts distances b/w O-O obeying if
  
    average_SiSi_bulk = np.mean(SiSi_bulk)
    std_SiSi_bulk = np.std(SiSi_bulk,dtype = np.float64)
    print 'BULK: The average Si-Si bond length & standard deviation:',average_SiSi_bulk,std_SiSi_bulk

    average_SiO_bulk = np.mean(SiO_bulk)
    std_SiO_bulk = np.std(SiO_bulk,dtype = np.float64)
    print 'BULK: The average Si-O bond length & standard deviation:',average_SiO_bulk,std_SiO_bulk

    average_OO_bulk = np.mean(OO_bulk)
    std_OO_bulk = np.std(OO_bulk,dtype = np.float64)
    print 'BULK: The average O-O bond length & standard deviation:', average_OO_bulk,std_SiO_bulk

if __name__=='__main__':
     main()
