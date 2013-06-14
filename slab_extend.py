#!/usr/bin/env python
#Program to extend a Ti,Si,O POSCAR inputfile, a slab, in the x and y direction, and output the new file,whihc contains only coordinates, atomtypes,etc mus tbe added by hand for now

import os,sys
import numpy as np

def main():

    inputfile = open('POSCAR1', 'r')
    outputfile = open('extend_POSCAR','w')

    #Read in line 1 of the POSCAR file:
    atom_type = inputfile.readline().split() #atom_type = [atom1,atom2,atom3,etc]
  
    inputfile.readline() #Skips line 2
    
    #Retrieve lattice constants from POSCAR file:
    x_lattice = float(inputfile.readline().split()[0]) #Reads in line 3    
    y_lattice = float(inputfile.readline().split()[1]) #Reads in line 4
    z_lattice = float(inputfile.readline().split()[2]) #Reads in line 5
   # print'lattices =', x_lattice,y_lattice,z_lattice
  
    inputfile.readline() #Skips 6th line,types of atoms
   
    #Read in line 7, defines how many of each type of atom
    natom_list = map(int,inputfile.readline().split()) #Reads in,stores,makes elements integers
    total_atoms = sum(natom_list)  #Sum of all atoms
 
    inputfile.readline() #Skips 8th line,Direct 
   
    x_array = []
    y_array = []
    z_array = [] 
    #Loop to separate into x,y,z arrays and convert Direct to Cartesian
    for i in range(total_atoms):
        line = inputfile.readline()
        if len(line.split()) > 0: #If not a blank line
            x_array.append(float(line.split()[0]))
            y_array.append(float(line.split()[1]))
            z_array.append(float(line.split()[2])) 
   # print x_array,y_array,z_array
    inputfile.close()
    
    #Convert columns to Cartesian:
    x_cartesian = [x * x_lattice for x in x_array] #Element wise multiplication
    y_cartesian = [y * y_lattice for y in y_array]
    z_cartesian = [z * z_lattice for z in z_array] 
    print 'x_cartesian=',x_cartesian  #,y_cartesian,z_cartesian     

    x_extension = []
    y_extension = []
    z_extension = [] 
   
    #Loops to create a copy of the cell in the x and y directions:
    for x in x_cartesian:
        x_extension.append(x + x_lattice) #Copy cell in positive x-dir'n
        
    for y in y_cartesian:
        y_extension.append(y + y_lattice) #Copy cell in positive y-dir'n

    for z in z_cartesian:
        z_extension.append(z) #Make a copy of z

    print 'x_extension=', x_extension
   
    #Need to order data,putting together coordinates based on atom type:
    atom_xcart = []
    atom_xext = []

    atom_ycart = []
    atom_yext = []

    atom_zcart = []
    atom_zext = []

    start_index = 0
    # Loops over x,y,z arrays and extensions to shift atom groups together
    for i in natom_list:
       
        end_index = start_index + natom_list[i]
        
        for j in np.arange(start_index,end_index):

            atom_xcart.append(x_cartesian[j]) #Extracts atom type i data from x_cartesian
            atom_xext.append(x_extension[j]) #Extracts atom type i data from x_extension

            ordered_x = atom_xcart + atom_xext # Puts together all atom type i xcoordinates
          
            atom_ycart.append(y_cartesian[j]) #Extracts atom type i data from y_cartesian
            atom_yext.append(y_extension[j]) #Extracts atom type i data from y_extension

            ordered_y = atom_ycart + atom_yext #Puts together all atom type i ycoordinates
           
            atom_zcart.append(z_cartesian[j]) #Extracts atom type i data from z_cartesian
            atom_zext.append(z_extension[j]) #Extracts atom type i data from z_extension
            
            ordered_z = atom_zcart + atom_zext #Puts together all atom type i zcoordinates

        start_index = end_index

    print 'atom_xcart=',atom_xcart
    print 'atom_xext =',atom_xext
    print 'orderedx=',ordered_x 
  
   # for i in range(len(ordered_newx)):
      #  print ordered_x[i], ordered_y[i], ordered_z[i]
    #    outputfile.write(str(ordered_x[i] + ' ' + str(ordered_y[i]) + ' ' + str(ordered_z[i]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
    main()
