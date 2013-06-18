#!/usr/bin/env python
#Program to extract coordinates from POSCAR file and delete first atom ,Ti
import os,sys
def main():
    inputfile = open('POSCAR', 'r')
    outputfile = open('slab2','w')
    
    #Skips first 6 lines in POSCaR file
    for line in range(6):
        line = inputfile.readline()
    #Read in total number of atoms
    natoms = sum(map(int,inputfile.readline().split())) 
    inputfile.readline() #skips line 8,Direct
    
    inputfile.readline()#skips atom 1, Ti

    #Reads in coordinates and writes it into outputfile without line spacing
    for atom in range(natoms - 1):
       line =  inputfile.readline()
       outputfile.write(line.strip() + '\n')
    
    inputfile.close()
    outputfile.close()
   
if __name__=='__main__':
    main() 
