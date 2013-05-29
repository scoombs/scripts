#!/usr/bin/env python
#Program to extend POSCAR inputfile, a slab, in the x and y direction, and output the new file
import os,sys
def main():

    inputfile = open('POSCAR', 'r')
    #outputfile = open('extend_POSCAR','w')

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
    print z_lattice

    #For now, skip over the line describing number of atoms:
    inputfile.readline() #skips 6th line,types of atoms
    inputfile.readline() #
    #for line in inputfile.readlines():
       
    inputfile.close()
    #outputfile.close()
if __name__=='__main__':
    main()
