#!/usr/bin/env python
#Program to extend a Direct POSCAR inputfile, a slab, in the x and y direction, and output the new extended POSCAR file 
import os,sys
import numpy as np

def main():
 
    #allow user input of the number of desired copies,ncopy
    try:
        program = sys.argv[0] #Gives filename
        ncopy = int(sys.argv[1])
    except IndexError:
        #Tell user what is required
        print '\nusage: '+program+' ncopy (where ncopy is an integer,number of desired cell copies)'
        #Exit program cleanly
        sys.exit(0)
    inputfile = open('POSCARfundy', 'r') 
    outputfile = open('extend_quartz90','w')

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
   # print x_cartesian
    x_extension = []
    y_extension = []
    z_extension = [] 
    for k in range(ncopy):
   
        for x in x_cartesian:
            for i in range(ncopy):#Want to order x-coordinates in the following way: x =[1,2,3] becomes x = [1,1..,1+lat,1+lat..1+n*lat,1+n*lat..,2,2..,2+lat,2+lat..]
                for j in range(ncopy):
                    x_extension.append( x + i*x_lattice) #Copy cell in x-dir'n,thru shifting over by +ing multipules of latt const.
        for y in y_cartesian:
        #Required to order y-coord, ie y = [1,2,3] becomes y = [1,1+lat,1+2*lat...,2,2+lat,...3,3+lat..]
            for i in range(ncopy):
                for j in range(ncopy):
                    y_extension.append(y + j*y_lattice) #Copy cell in positive y-dir'n

        for z in z_cartesian:
            for i in range(ncopy):
                for j in range(ncopy):# Want to order it so each copy of atomtype n has the original z coordinates
                    z_extension.append(z + k*z_lattice) #Make a copy of z
                    
   # print x_extension,len(x_extension)#length = total_natoms*ncopy^2
   # print y_extension,len(y_extension)
   # print z_extension,len(z_extension)

    #Need to order data,putting together coordinates based on atom type:
   # ordered_x = []
   # ordered_y = []
   # ordered_z = []
  
   # start_index = 0
  # Loops over x,y,z arrays and extensions to shift atom groups together
   # for i in range(len(natom_list)):
   
    #    end_index = start_index + ncopy**2*natom_list[i]
        #atom_xcart = []
     #   x_ext = []
 
        #atom_ycart = []
      #  y_ext = []
 
        #atom_zcart = []
       # z_ext = []
        #This loop changed "window" depending on the number of each type of atom 
        #for j in np.arange(start_index,end_index):

         #   x_ext.append(x_extension[j])  #Extracts atom type i data from x_extension

          #  y_ext.append(y_extension[j])  #Extracts atom type i data from y_extension
           
    #        z_ext.append(z_extension[j])  #Extracts atom type i data from z_extension

     #       start_index = end_index

      #  ordered_x.extend(x_ext) #Put all x data into correct order based on atom type
       # ordered_y.extend(y_ext) #Put all x data into correct order based on atom type
        #ordered_z.extend(z_ext) #Put all x data into correct order based on atom type
       # ordered_y.extend( atom_yext) #Puts together all atom type i ycoordinates
       # ordered_z.extend( atom_zext) #Puts together all atom type i zcoordinates
   

    #Formatting the output file to be POSCAR-like:

    #Writes out atom types on line 1:
    for i in range(len(atom_type)):
        outputfile.write(str(atom_type[i]) + ' ')
   
    outputfile.write('\n'+ ' ' + ' ' + str(1.00000)+ '\n')#Writes a 1.00000 on line 2
    outputfile.write(' ' + ' ' + str(x_lattice*ncopy) +' '+ str(0.00) +' '+ str(0.00) + '\n') #Writes out x_lattice on line 3
    outputfile.write(' ' + ' ' + str(0.00) +' '+ str(y_lattice*ncopy) +' '+str(0.00) + '\n') #Writes y_lattice on line 4
    outputfile.write(' ' + ' ' + str(0.00) +' '+ str(0.00) +' '+ str(z_lattice*ncopy) + '\n') #Writes z_lattice on line 5
   
    #Writes out atom types on line 6: 
    for i in range(len(atom_type)):
        outputfile.write(' ' + str(atom_type[i]))

    outputfile.write('\n') #Skips to line 7
    #Writes out number of each atom on line 7:
    for i in range(len(natom_list)):
        outputfile.write(' '+ ' '+ str(ncopy**3*(natom_list[i])))#ADJUST THIS NUMBERING LATER,AFTER ASSIGNING A NAME TO NCOPY

    outputfile.write('\n' + str('Cartesian')+ '\n') #Writes Cartesian on line 8
     
    #Formatting for the output file,puts lists into x,y,z columns 
    for i in range(len(x_extension)):
       # print ordered_x[i], ordered_y[i], ordered_z[i]
        outputfile.write(str(x_extension[i]) + ' ' + str(y_extension[i]) + ' ' + str(z_extension[i]) + '\n')
    
    outputfile.close()
if __name__=='__main__':
     main()
