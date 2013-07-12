#!/usr/bin/env python 
#This program reads in an xyz file & outputs two xyz files, one for surface atoms, and one with the bulk atoms
import os,sys
import numpy as np

def main():
    
    #Allow user input of surface width:
    try:
        program = sys.argv[0] #Gives filename
        width = float(sys.argv[1])
    except IndexError:
        #Tell user what is needed
        print '\n usage: '+program+' width (where the units are in angstrom,1 nanometer = 10 angstrom)'
        sys.exit(0)

    #Allow user to input file name from terminal:
    filein = raw_input("Enter filename (xyz format):")
    inputfile = open(filein, 'r')

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
    z = []
    for i in range(natoms):
        atom = atoms[i]
        z.append(float(atom[3]))
    max_z = max(z)
    #print max_z

    #Loop over atoms & seperate them based on the "width" of surface given
    for i in range(natoms):
        atom = atoms[i]
        z_diff = abs(float((atom[3] - max_z)))
        if z_diff <= width:
            surf_outputfile.write(str(atom[0]) + ' '+ str(atom[1]) + ' ' + str(atom[2]) + ' ' + str(atom[3]) + '\n')
        if z_diff > width:
            bulk_outputfile.write(str(atom[0]) + ' '+ str(atom[1]) + ' ' + str(atom[2]) + ' ' + str(atom[3]) + '\n')

    surf_outputfile.close()
    bulk_outputfile.close()


if __name__=='__main__':
    main() 
