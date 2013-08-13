#!/usr/bin/env python

#Program used to calculate atom's nearest neighbours, to plot spacially

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
        nbins = float(sys.argv[5])
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice z-lattice first_gr_minimum nsteps nbins \n'
        #Exit program cleanly
        sys.exit(0)

    #Allow user to input file name from terminal:
    filein = raw_input("Enter filename (xyz format):")
    inputfile = open(filein, 'r')
    
    #The following will be used to plot nn distances spacially ( using a histogram)
    bin_width = (lattice_z)/float(nbins)
    nn_bins = np.zeros(nbins,dtype = float) #Initialize array to store nn count in bins based on z-coordinate
    count_bins = np.zeros(nbins,dtype = int) # Initialize arrays that will store number of items in each bin
 
    for n in range(nsteps): #Time step loop

        natoms = int(inputfile.readline().strip()) #Reads in number of atoms 
        inputfile.readline() #Reads line2, blank space
       
        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
            atoms.append(line.split()) #Appends lists of atom coordinates [TYPE,x,y,z],to be used in distances array

        #Loops to find the distance between any two atoms
        distances = np.zeros((natoms,natoms),dtype = float) 
        for i in range(natoms): #Loops over first atom in the atom pairs
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
   
                distances[i][j] = (x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.)
        #print distances,type(distances[0][0])
        #Loop through the distance matrix & determine number of nearest neighbours per atom
    
        for i in range(natoms):
        
            ifdist = [] #Temporary array for nn distance storage

            for j in range(natoms):#Loop through each element in row
                if distances[i,j] > 0.0001 and distances[i,j] < first_minimum:  #First minima of the g(r) function
                    ifdist.append(distances[i,j]) #Extracts all distance in col. i that obey if statement
            row_nn = len(ifdist) #Determines the number of distances obeying if
            bin = int(float(atoms[i][3])/float(bin_width))
#            print bin, row_nn
            nn_bins[bin] += row_nn  #Adds nn to the approporiate bin
            count_bins[bin] += 1 #Adds a value of 1 for each time a nn count falls into a certain bin 
 
#        print nn_bins
#        print count_bins
    
    #Print plotting information to outputfile: 
   # outputfile = open('TESTnn_spacialplot.dat' ,'w')

    nn_spacial = []
    bin_edges = []
    middle = []
    for i in range(int(nbins)):    
        #Recall: bin_width = (lattice_z)/(nbins) , lattice_z being maximum z value, minimum being 0
        bin_edges.append(bin_width*i)
        left = bin_edges[i]
        right = bin_width + left
        middle.append((left+right)/2.) #Finds the middle of each bin, to be used as x-axis in plot
        if count_bins[i] > 0:
            nn_spacial.append(nn_bins[i]/float(count_bins[i]))
        else:
            nn_spacial.append(nn_bins[i])
   # print nn_spacial,len(nn_spacial)
   # print middle,len(middle)
       # outputfile.write(str(middle[i]) + ' ' + str(nn_spacial[i]) + '\n')
    inputfile.close()
   # outputfile.close()    
    
    #Find the average number of nearest neighbours:
#    average_nn = np.mean(nn)
#    print 'The average number of nearest neighbours is:',average_nn
    #Find the standard deviation: std = sqrt(mean(abs(x - x.mean())**2))
#    std_dev = np.std(nn,dtype = np.float64)
#    print 'The standard deviation is:',std_dev
    

if __name__=='__main__':
     main()
