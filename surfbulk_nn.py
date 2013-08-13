#!/usr/bin/env python

#Program reads in an SiO2 xyz file & calculates number of nearest neighbours in surface Si,O & bulk Si,O atoms

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
        width = float(sys.argv[5])
     
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice first_gr_minimum nsteps width (where lattice & nsteps & nbins are floats)\n'
        #Exit program cleanly
        sys.exit(0)

    #Allow user to input file name from terminal:
    filein = raw_input("Enter filename (xyz format):")
    inputfile = open(filein, 'r')
    
    
    for n in range(nsteps): #Time step loop

        natoms = int(inputfile.readline().strip()) #Reads in number of atoms
        #print natoms
        inputfile.readline() #Reads line2, blank space

        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
            atoms.append(line.split()) #Appends lists of atom coordinates [TYPE,x,y,z]
        #print atoms
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
       # print max_z
        distances = np.zeros((natoms,natoms),dtype=float)
        #To loop over only all pairs of atoms:
        for i in range(natoms):
            atom1 = atoms[i]

            for j in range(natoms):#Loops over second atom,doesn't account for duplicates
                atom2 = atoms[j]
          
                #Finds the difference between x,y,z coordinates of each pair:
                x_pair_diff = float(atom1[1]) - float(atom2[1])
                y_pair_diff = float(atom1[2]) - float(atom2[2])
                z_pair_diff = float(atom1[3]) - float(atom2[3])
                print z_pair_diff
                #Need to consider affects of periodic boundary conditions:
                x_pair_diff -= lattice_x*pbc_round(x_pair_diff/lattice_x)
                y_pair_diff -= lattice_y*pbc_round(y_pair_diff/lattice_y)
                z_pair_diff -= lattice_z*pbc_round(z_pair_diff/lattice_z)
               
                distances[i][j] = (x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.)
                
        #Separate surface & bulk,captures indices for atoms that obey statements
        surface = []
        bulk = []
        for i in range(len(atoms)):
            z_diff = abs(float((atoms[i][3] - max_z)))
            if z_diff <= width:
                surface.append(i) #This gives COLUMN indices for surface atoms
            else:
                bulk.append(i)
        print'bulk=', bulk
        print 'surf = ',surface,len(surface),natoms
    
        #NEAREST NEIGHBOURS FOR SURFACE ATOMS:

        tmp = []
        nnSi_surface = []
        nnO_surface = []
        for j in surface: # Loop through all surface atoms column indices
           if atoms[j][0] == 'Si':
                #print atoms[j]
                for i in np.arange(natoms):
                #print distances[i,j]
                    if distances[i,j] > 0.0001 and distances[i,j] < first_minimum: #Finds nearest neighbours for surface Si
                        tmp.append(distances[i]) #Extracts all distances that obey if
                    #print tmp
                        row = len(tmp) #Determines number of distances obeying if
                tmp[:] = [] #Clears tmp before moving to the next row
                nnSi_surface.append(row)
           else: #Will loop over remaining surface atoms (the oxygens)
                for i in range(natoms):
                    if distances[i,j] > 0.0001 and distances[i,j] < first_minimum: #Finds nearest neighbours for surface O
                        tmp.append(distances[i]) #Extracts all distances that obey if
                        row = len(tmp) #Determines number of distances obeying if
                tmp[:] = [] #clears tmp before moving to next row
                nnO_surface.append(row)
        print'nn_Sisurface = ', nnSi_surface 
        #print 'nn_Osurface = ' , nnO_surface
    
        #print type(nnSi_surface[0]) 
        #Find avg number of Si surface nearest neighbours:
        nn_surfaceSi = np.mean(nnSi_surface,dtype = np.float64)
        print 'The avg # of surface Si nearest neighbours is:', nn_surfaceSi
        #Find the avg number of O surface nearest neighbours: 
        nn_surfaceO = np.mean(nnO_surface,dtype = np.float64)
        print 'The avg # of surface O nearest neighbours is:',nn_surfaceO 
    
        #NEAREST NEIGHBOURS FOR BULK ATOMS:    

        nnSi_bulk = []
        nnO_bulk = []
    
        for j in bulk: # Loop through all bulk atoms column indices
            if atoms[j][0] == 'Si':
                #print 'bulksi=',atoms[j]
                for i in np.arange(natoms):
                    if distances[i,j] > 0.0001 and distances[i,j] < first_minimum: #Finds nearest neighbours for bulk Si
                        tmp.append(distances[i]) #Extracts all distances that obey if
                        row = len(tmp) #Determines number of distances obeying if
                tmp[:] = [] #Clears tmp before moving to the next row
                nnSi_bulk.append(row)
            else: #Will loop over remaining bulk atoms (the oxygens)
                for i in range(natoms):
                    if distances[i,j] > 0.0001 and distances[i,j] < first_minimum: #Finds nearest neighbours for bulk  O
                        tmp.append(distances[i]) #Extracts all distances that obey if
                        row = len(tmp) #Determines number of distances obeying if
                tmp[:] = [] #clears tmp before moving to next row
                nnO_bulk.append(row)
        #print 'nn_Sibulk =',nnSi_bulk
        #print 'nn_Obulk =',nnO_bulk

    #Find the avg number of Si bulk nn:
        nn_bulkSi = np.mean(nnSi_bulk,dtype = np.float64)
        print 'The avg # of bulk Si nn is:',nn_bulkSi
    #Find the avg number of O bulk nn:
        nn_bulkO = np.mean(nnO_bulk,dtype = np.float64)
        print 'The avg # of bulk O nn is:',nn_bulkO


 

if __name__=='__main__':
     main()
