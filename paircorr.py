#!/usr/bin/env python
#Computes pair correlation function,g(r),taking *.xyz input file
import os,sys
import numpy as np 
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
    """
    This is the main function.
    """
    #Allow the user to input the periodic boundary condiotns (box size) and number of bins to be used:
    try:
        program =sys.argv[0] #Gives filename
        lattice = float(sys.argv[1])
        lattice_x = lattice #int(sys.argv[1])
        lattice_y = lattice #int(sys.argv[2])
        lattice_z = lattice #int(sys.argv[3])
        nsteps = int(sys.argv[2])
        nbins = int(sys.argv[3])
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' lattice nsteps  nbins (where lattice & nsteps & nbins are integers)\n' 
        #Exit program cleanly
        sys.exit(0)

    inputfile = open( 'output_1000k_96_again.xyz' , 'r')
    outfile = open('10000k_96_quartz_again' , 'w')
   
    #Timestep loop
    distances = []
 
    for n in range(nsteps):

        natoms = int(inputfile.readline().split()[0])  #Reads line 1,number of atoms
        inputfile.readline() #Reads line 2, blank space
  
        atoms = []
        for i in range(natoms):
            line = inputfile.readline()
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
                x_pair_diff = float(atom1[0]) - float(atom2[0])
                y_pair_diff = float(atom1[1]) - float(atom2[1])
                z_pair_diff = float(atom1[2]) - float(atom2[2])        
               # print 'atom1[i],atom2[i],x_pair_diff=',atom1[2], atom2[2],z_pair_diff
            
                #Need to consider affects of periodic boundary conditions:
                x_pair_diff -= lattice_x*pbc_round(x_pair_diff/lattice_x)
                y_pair_diff -= lattice_y*pbc_round(y_pair_diff/lattice_y)
                z_pair_diff -= lattice_z*pbc_round(z_pair_diff/lattice_z)
               # print x_pair_diff    
                distances.append((x_pair_diff**2 + y_pair_diff**2 + z_pair_diff**2)**(1./2.))
#               print distances
   
    hist,bin_edges = np.histogram(distances,bins=nbins, range=(0,lattice/2))
    hist = hist/float(nsteps) 

    #Prepares an x column,bin_edges and y_column hist, which can plot a histogram in gnuplot
    for i in range(len(hist)):
       # print bin_edges[i], hist[i]

        #Determine density of atoms that lie within donuts, dr, with inner radius r_right & outer r_left
        bin_width = (lattice/2.)/(nbins)
        r_left = bin_edges[i]
        r_right = bin_width + r_left
       
        vol_shell = (4./3.)*np.pi*(r_right**3) - (4./3.)*np.pi*(r_left**3) #difference in volumes of 2 spheres 
        #print dr
        #According to wiki: use g(r) = 4*np.pi*r**2*dr, integrates to 4/3 pi (r_b**3 - r_a**3)

        density = hist[i]/vol_shell
        r = (r_left + r_right)*(1./2.) #Average of bin,to be used in plot r vs v
        print r,density

#        print bin_edges[i],vol_shell 

# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
