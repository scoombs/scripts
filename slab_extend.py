#!/usr/bin/env python
#Program to extend a Direct POSCAR inputfile, a slab, in the x and y direction, and output the new extended POSCAR file 
import os,sys
import numpy as np

def main():

    inputfile = open('POSCARfundy', 'r')
    outputfile = open('extend_POSCAR1','w')

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
    print y_cartesian
    x_extension = []
    y_extension = []
    z_extension = [] 
   
    for i in range(3):  
        for j in range(3): #change 3 to number of copies you want,just testing now
            for x in x_cartesian:
               x_extension.append(x + j*x_lattice) #Copy cell in positive x-dir'n
               x_extension = sorted(x_extension) # Sorts in increasing order 
            for y in y_cartesian:
                y_extension.append(y + j*y_lattice) #Copy cell in positive y-dir'n
            for z in z_cartesian:
                z_extension.append(z) #Make a copy of z
   
    print x_extension,len(x_extension)
    print y_extension,len(y_extension)
    print z_extension,len(z_extension)
    #Need to order data,putting together coordinates based on atom type:
    ordered_x = []
    ordered_y = []
    ordered_z = []
  
    start_index = 0
  # Loops over x,y,z arrays and extensions to shift atom groups together
    for i in range(len(natom_list)):
   
        end_index = start_index + natom_list[i]
        atom_xcart = []
        atom_xext = []
 
        atom_ycart = []
        atom_yext = []
 
        atom_zcart = []
        atom_zext = []
        #This loop changed "window" depending on the number of each type of atom 
        for j in np.arange(start_index,end_index):

            atom_xcart.append(x_cartesian[j]) #Extracts atom type i data from x_cartesian
            atom_xext.append(x_extension[j])  #Extracts atom type i data from x_extension
            atom_ycart.append(y_cartesian[j]) #Extracts atom type i data from y_cartesian
            atom_yext.append(y_extension[j])  #Extracts atom type i data from y_extension

           
            atom_zcart.append(z_cartesian[j]) #Extracts atom type i data from z_cartesian
            atom_zext.append(z_extension[j])  #Extracts atom type i data from z_extension
            start_index = end_index

        ordered_x.extend(atom_xcart + atom_xext) #Put all x data into correct order based on atom type
        ordered_y.extend(atom_ycart + atom_yext) #Puts together all atom type i ycoordinates
        ordered_z.extend(atom_zcart + atom_zext) #Puts together all atom type i zcoordinates
        print atom_xext
    #Formatting the output file to be POSCAR-like:

    #Writes out atom types on line 1:
    for i in range(len(atom_type)):
        outputfile.write(str(atom_type[i]) + ' ')
   
    outputfile.write('\n'+ ' ' + ' ' + str(1.00000)+ '\n')#Writes a 1.00000 on line 2
    outputfile.write(' ' + ' ' + str(x_lattice) +' '+ str(0.00) +' '+ str(0.00) + '\n') #Writes out x_lattice on line 3
    outputfile.write(' ' + ' ' + str(0.00) +' '+ str(y_lattice) +' '+str(0.00) + '\n') #Writes y_lattice on line 4
    outputfile.write(' ' + ' ' + str(0.00) +' '+ str(0.00) +' '+ str(z_lattice) + '\n') #Writes z_lattice on line 5
   
    #Writes out atom types on line 6: 
    for i in range(len(atom_type)):
        outputfile.write(' ' + str(atom_type[i]))

    outputfile.write('\n') #Skips to line 7
    #Writes out number of each atom on line 7:
    for i in range(len(natom_list)):
        outputfile.write(' '+ ' '+ str(2*natom_list[i]))

    outputfile.write('\n' + str('Cartesian')+ '\n') #Writes Cartesian on line 8
     
    #Formatting for the output file,puts lists into x,y,z columns 
    for i in range(len(ordered_x)):
       # print ordered_x[i], ordered_y[i], ordered_z[i]
        outputfile.write(str(ordered_x[i]) + ' ' + str(ordered_y[i]) + ' ' + str(ordered_z[i]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
    main()
