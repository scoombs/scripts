#!/usr/bin/env python 
#This program reads in an xyz file & outputs two xyz files, one for surface atoms, and one with the bulk atoms
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

    #Allow user input of suraface width:
    try:
        program = sys.argv[0] #Gives filename
        lattice = float(sys.argv[1])
        width = float(sys.argv[2])
    except IndexError:
        #Tell user what is needed
        print '\n usage: '+program+' lattice width (where the units are in angstrom,1 nanometer = 10 angstrom)'
        sys.exit(0)
 
    inputfile = open('quartz324.xyz','r')
    surf_outputfile = open('surf.xyz','w')
    bulk_outputfile = open('bulk.xyz','w')
   
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

    #First find the maximum z value:
    for i in range(natoms):
        atom = atoms[i]
        z.append(float(atom[3]))
    max_z = max(z)
    
    #Loop over atoms & write out only those where z-coordinate  max - width < z < max
    for i in range(natoms):
        atom = atoms[i]
        z_diff = abs(float((atom[3] - max_z)))
        if z_diff <= width
            surf_outputfile.write(str(atom[0]) + ' '+ str(atom[1]) + ' ' + str(atom[2]) + ' ' + str(atom[3]) + '\n')
    surf_outputfile.close()


if __name__=='__main__':
    main() 
