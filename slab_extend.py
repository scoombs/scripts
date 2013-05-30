#!/usr/bin/env python
#Program to extend POSCAR inputfile, a slab, in the x and y direction, and output the new file
import os,sys
def main():

    inputfile = open('POSCAR', 'r')
    outputfile = open('extend_POSCAR','w')

    #Want to skip over the first 2 lines of the POSCAR file
    inputfile.readline() #skips 1st line
    inputfile.readline() #skips 2nd line
    
    #Retrieve lattice constants from POSCAR file:
    line3 = inputfile.readline()
    x_lattice = float(line3.split()[0])
    #NOTE:if not orthonormal,could have made this into an array x_lattice= [all that stuff] 
    line4 = inputfile.readline()
    y_lattice = float(line4.split()[1])
    line5 = inputfile.readline()
    z_lattice = float(line5.split()[2])
    
    #For now, skip over the line describing number of atoms:
    inputfile.readline() #skips 6th line,types of atoms
    inputfile.readline() #skips 7th line,number of atoms
    inputfile.readline() #skips 8th line,Direct 
    
    x_array = []
    y_array = []
    z_array = [] 
    #Loop to convert direct to cartesian and separate into x,y,z arrays
    for line in inputfile:
        #Retrieve columns from POSCAR (remember to remove spacing in file) 
        x_array.append(float(line.split()[0]))
        y_array.append(float(line.split()[1]))
        z_array.append(float(line.split()[2])) 
    inputfile.close()
    
    #Convert columns to Cartesian:
    x_cartesian =[ x * x_lattice for x in x_array] #element wise multiplication
    y_cartesian = [y * y_lattice for y in y_array]
    z_cartesian = [z * z_lattice for z in z_array] 
        

    x_extension = []
    y_extension = []
  # z_extension = [] code can easily be modified to extend in z-dir'n   
    #Loops to create a copy of the cell in the x and y directions:
    x_extension =[x + x_lattice for x in x_cartesian] #copy cell in positive x-dir'n
    y_extension = [y + y_lattice for y in y_cartesian] #copy cell in positive y-dir'n
  # z_extension = [z + z_lattice for z in z_cartesian]


    #Concatinate the original x_cartesian to x_extension:
    new_xcoordinates = x_cartesian + x_extension
      
    #Concatinate y_cartesian to y_extension:
    new_ycoordinates = y_cartesian + x_cartesian

    for i in range(len(new_xcoordinates)):
#        print new_xcoordinates[i], new_ycoordinates[i], z_cartesian[i%len(z_cartesian)]
        outputfile.write(str(new_xcoordinates[i]) + ' ' + str(new_ycoordinates[i]) + ' ' + str(z_cartesian[i%len(z_cartesian)]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
    main()
