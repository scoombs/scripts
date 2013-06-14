#!/usr/bin/env python
#Program to extend a Ti,Si,O POSCAR inputfile, a slab, in the x and y direction, and output the new file,whihc contains only coordinates, atomtypes,etc mus tbe added by hand for now

import os,sys
def main():

    inputfile = open('POSCAR1', 'r')
    outputfile = open('extend_POSCAR','w')

    #Read in the first line of the POSCAR file:
    line1 = inputfile.readline() 
    atom1 = str(line1.split()[0]) #reads in atom type 1
    atom2 = str(line1.split()[1]) #reads in atom type 2
    atom3 = str(line1.split()[2]) #reads ina tom type 3
   # print atom1,atom2,atom3
    inputfile.readline() #skips 2nd line
    
    #Retrieve lattice constants from POSCAR file:
   
    x_lattice = float(inputfile.readline().split()[0]) #reads in line 3
    #NOTE:if not orthonormal, make this into an array x_lattice= [float(line3.split()[0]] 
   
    y_lattice = float(inputfile.readline().split()[1]) #reads in line 4
   
    z_lattice = float(inputfile.readline().split()[2]) #reads in line 5
    # print x_lattice,y_lattice,z_lattice
  
    inputfile.readline() #skips 6th line,types of atoms
   
    #Read in line defining how many of each type of atom, to be used in loop later on
    line7 = inputfile.readline() #Reads 7th line,number of atoms
    natom1 = int(line7.split()[0]) #Reads in number of atoms type 1
    natom2 = int(line7.split()[1]) #Reads in number of atoms type 2
    natom3 = int(line7.split()[2]) # Reads in number of atoms type 3
   # print natom1,natom2,natom3

    inputfile.readline() #skips 8th line,Direct 
   
    x_array = []
    y_array = []
    z_array = [] 
    #Loop to separate into x,y,z arrays and convert Direct to Cartesian
    for line in inputfile:
        if len(line.split()) > 0:
        #Retrieve columns from POSCAR (remember to remove spacing in file) 
            x_array.append(float(line.split()[0]))
            y_array.append(float(line.split()[1]))
            z_array.append(float(line.split()[2])) 
   # print x_array,y_array,z_array
    inputfile.close()
    
    #Convert columns to Cartesian:
    x_cartesian = [x * x_lattice for x in x_array] #element wise multiplication
    y_cartesian = [y * y_lattice for y in y_array]
    z_cartesian = [z * z_lattice for z in z_array] 
   # print x_cartesian,y_cartesian,z_cartesian     

    x_extension = []
    y_extension = []
  # z_extension = [] code can easily be modified to extend in z-dir'n
   
    #Loops to create a copy of the cell in the x and y directions:
    x_extension =[x + x_lattice for x in x_cartesian] #copy cell in positive x-dir'n
    y_extension = [y + y_lattice for y in y_cartesian] #copy cell in positive y-dir'n
  # z_extension = [z + z_lattice for z in z_cartesian]
   # print x_extension,y_extension

    #Concatinate the original x_cartesian to x_extension:
    new_xcoordinates = x_cartesian + x_extension
     
    #Concatinate y_cartesian to y_extension:
    new_ycoordinates = y_cartesian + y_extension

   # print new_xcoordinates,new_ycoordinates     

    for i in range(len(new_xcoordinates)):
      #  print new_xcoordinates[i], new_ycoordinates[i], z_cartesian[i%len(z_cartesian)]
        outputfile.write(str(new_xcoordinates[i]) + ' ' + str(new_ycoordinates[i]) + ' ' + str(z_cartesian[i%len(z_cartesian)]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
    main()
