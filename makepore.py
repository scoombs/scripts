#!/usr/bin/env python
#This program reads in an xyz file(units= angstrom) & removes a hole out of the centre with radius specified by user in angstroms
import os,sys
import numpy as np
def main():
    
    #Allow user input of hole radius:
    try:
        program = sys.argv[0] #Gives filename
        radius = float(sys.argv[1])
    except IndexError:
        #Tell user what is needed
        print '\n usage: '+program+' radius (where radius is in angstrom,1 nanometer = 10 angstrom)'
        sys.exit(0)
 
    inputfile = open('test0.xyz','r')
    outputfile = open('test_hole.xyz','w')
   
    natoms = int(inputfile.readline().strip()) #Reads in number of atoms
    #print natoms,type(natoms)
    inputfile.readline() #Skips line 2 (blank/comment line)

    #First need to find the centre of the bulk given:
    #Create 3 arrays: x,y,z
   # x = []
  #  y = []
   # z = []
    #for i in range(natoms):
     #   line = inputfile.readline()
      #  x.append(float(line.split()[1]))
       # y.append(float(line.split()[2]))
        #z.append(float(line.split()[3]))
    atoms = []
    for i in range(natoms):
        line = inputfile.readline()
        tmp = line.split() # Splits list
        tmp.pop(0) # Pops off first entry in each list (atom type)
        atoms.append(tmp) # Appends lists of atom coordinates together
    print atoms
    inputfile.close()
    #COnvert elements to floats instead of strings:
    for row in atoms:
        for i in range(len(row)):
            row[i] = float(row[i])
    print atoms
    inputfile.close()

    
    #First need to find the centre of the bulk given:
    x_center = sum(atoms[0])/natoms
    y_center = sum(atoms[1])/natoms
    z_center = sum(atoms[2])/natoms
    print x_center,y_center,z_center
   
    #Circle's center is (x_center,y_center,z_center)
    
    
   
        
    




if __name__=='__main__':
    main() 
