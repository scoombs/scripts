#!/usr/bin/env python
#Program to extend a Ti,Si,O POSCAR inputfile, a slab, in the x and y direction, and output the new file,whihc contains only coordinates, atomtypes,etc mus tbe added by hand for now

import os,sys
import numpy as np

def main():

    inputfile = open('POSCAR1', 'r')
    outputfile = open('extend_POSCAR','w')

    #Read in the first line of the POSCAR file:
    line1 = inputfile.readline() 
    #atom_type = [inputfile.readline().split()]
    atom1 = str(line1.split()[0]) #reads in atom type 1
    atom2 = str(line1.split()[1]) #reads in atom type 2
    atom3 = str(line1.split()[2]) #reads in atom type 3
    
    atom_type = [atom1,atom2,atom3]
   
    inputfile.readline() #skips 2nd line
    
    #Retrieve lattice constants from POSCAR file:
    x_lattice = float(inputfile.readline().split()[0]) #reads in line 3    
    y_lattice = float(inputfile.readline().split()[1]) #reads in line 4
    z_lattice = float(inputfile.readline().split()[2]) #reads in line 5
    print'lattices =', x_lattice,y_lattice,z_lattice
  
    inputfile.readline() #skips 6th line,types of atoms
   
    #Read in line defining how many of each type of atom, to be used in loop later on
    line7 = inputfile.readline() #Reads 7th line,number of atoms
    natom1 = int(line7.split()[0]) #Reads in number of atoms type 1
    natom2 = int(line7.split()[1]) #Reads in number of atoms type 2
    natom3 = int(line7.split()[2]) #Reads in number of atoms type 3
    natom_list = [natom1,natom2,natom3]
    total_atoms = np.sum(natom_list)  #Sum of all atoms
   
   # print natom1,natom2,natom3,total_atoms

    inputfile.readline() #skips 8th line,Direct 
   
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
    x_cartesian = [x * x_lattice for x in x_array] #element wise multiplication
    y_cartesian = [y * y_lattice for y in y_array]
    z_cartesian = [z * z_lattice for z in z_array] 
    print y_cartesian #,y_cartesian,z_cartesian     

    x_extension = []
    y_extension = []
    z_extension = [] #code can easily be modified to extend in z-dir'n
   
    #Loops to create a copy of the cell in the x and y directions:
    for x in x_cartesian:
        x_extension.append(x + x_lattice) #copy cell in positive x-dir'n
        
    for y in y_cartesian:
        y_extension.append(y + y_lattice) #copy cell in positive y-dir'n

    for z in z_cartesian:
        z_extension.append(z) #make a copy

    print 'y_exten=', y_extension
   
    #Need to order data,putting together coordinates based on atom type:
    atom_xcart = []
    atom_xext = []
    atom_ycart = []
    atom_yext = []
    atom_zcart = []
    atom_zext = []

    start_index = 0

    for i in natom_list:
        print natom_list[i]
   
        end_index = start_index + natom_list[i]
        
        for j in np.arange(start_index,end_index):

            atom_xcart.append(x_cartesian[j]) #Extracts atom type i data from x_cartesian
            atom_xext.append(x_extension[j]) #Extracts atom type i data from x_extension
            ordered_newx = atom_xcart + atom_xext # Puts together all atom type i xdata
           # print 'newx=',atom1_newx
            atom_ycart.append(y_cartesian[j]) 
            atom_yext.append(y_extension[j])
            ordered_newy = atom1_ycart + atom1_yext #Puts together all atom type 1 ydata

        start_index = end_index
        print 'newy=',atom_newy   
        print 'atom_ycart=',atom_ycart   
   # for i in range(len(new_xcoordinates)):
      #  print new_xcoordinates[i], new_ycoordinates[i], z_cartesian[i%len(z_cartesian)]
    #    outputfile.write(str(new_xcoordinates[i]) + ' ' + str(new_ycoordinates[i]) + ' ' + str(z_cartesian[i%len(z_cartesian)]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
    main()
