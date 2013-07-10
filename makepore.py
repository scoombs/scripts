#!/usr/bin/env python
#This program reads in an xyz file(units= angstrom) & removes a hole out of the centre with radius specified by user in angstroms
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
    
    #Allow user input of hole radius:
    try:
        program = sys.argv[0] #Gives filename
        radius = float(sys.argv[1])
        lattice = float(sys.argv[2]) 
    except IndexError:
        #Tell user what is needed
        print '\n usage: '+program+' radius lattice (where radius is in angstrom,1 nanometer = 10 angstrom)'
        sys.exit(0)
 
    inputfile = open('quartz324.xyz','r')
    outputfile = open('324pore_pbcTEST.xyz','w')
   
    natoms = int(inputfile.readline().strip()) #Reads in number of atoms
    inputfile.readline() #Skips line 2 (blank/comment line)

    atoms = []
    for i in range(natoms):
        line = inputfile.readline()
        atoms.append(line.split()) # Appends lists of atom coordinates together
 
    inputfile.close()

    #Convert elements to floats instead of strings: (Note: each 'row' is a set of coordinates for an atom: (TYPE,x,y,z))
    for row in atoms:
        for i in np.arange(1,len(row)):
            row[i] = float(row[i])
  
    #First need to find the centre of the bulk given:
    x_center = sum(row[1] for row in atoms)/natoms #Need to pick out the correct term, all the x's 
    y_center = sum(row[2] for row in atoms)/natoms
    z_center = sum(row[3] for row in atoms)/natoms
   # print x_center,y_center,z_center
    
    #Circle's center is (x_center,y_center,z_center)
    #Will loop over distance b/w an atom & the center of the circle
    for i in range(natoms):
        atom2 = atoms[i]
        pair_diff = abs(float(((atom2[1] - x_center)**2. + (atom2[2] - y_center)**2.)**(1./2.))) #Subtracts x-y Euclidean distances
        
        #Consider periodic boundary conditions,
        pair_diff -= lattice*pbc_round(pair_diff/lattice)

        if pair_diff >= radius: 
            outputfile.write( str(atom2[0]) + ' '+ str(atom2[1]) + ' ' + str(atom2[2]) + ' ' + str(atom2[3]) + '\n')
    print  'Distance between pores is:',lattice - radius*2
    outputfile.close()
      
if __name__=='__main__':
    main() 
