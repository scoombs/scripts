#!/usr/bin/env python
#Program will only keep first timestep of xyz file 
import os,sys
def main():

    inputfile = open('cooldown.xyz', 'r')
    outputfile = open('cooldown_1ts.xyz','w')

    natoms = int(inputfile.readline().split()[0]) #reads in number of atoms, line 1
    inputfile.readline()
    print natoms
    x_array = []
    y_array = []
    z_array = []
    atomtype = []
    for line in range(natoms):
        line = inputfile.readline()
        atomtype = str(line.split()[0])
        x_array = float(line.split()[1])
        y_array = float(line.split()[2])
        z_array = float(line.split()[3])
        outputfile.write(str(atomtype) + ' ' + str(x_array) + ' ' + str(y_array) + ' ' + str(z_array) + '\n')
    inputfile.close()
    outputfile.close()
   
if __name__=='__main__':
    main() 
