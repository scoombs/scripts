#!/usr/bin/env python
#Program to extract coordinates from slab2_Ti POSCAR file and delete first atom ,Ti.
#Then orders file so it has *.gen formatting
import os,sys
import numpy as np
def main():
    inputfile = open('POSCAR', 'r')
    outputfile = open('slab2','w')
    
    #Skips first 2 lines in POSCAR file
    inputfile.readline()
    inputfile.readline() 
    
    #This will be needed for periodic condtions at the end of the *.gen file
    xlatt_line = inputfile.readline().strip()
    ylatt_line = inputfile.readline().strip()
    zlatt_line = inputfile.readline().strip()
    
    inputfile.readline() #Skips type of atom line

    #Read in total number of each atom
    natoms = map(int,inputfile.readline().split())
    total_atoms =sum(natoms) #calculates total number of atoms 
 
    inputfile.readline() #skips line 8,Direct
    
    inputfile.readline()#skips atom 1, Ti

    #Write out in format of *.gen file
    # type "F" means same thing as Direct
    outputfile.write(str(total_atoms-1) + ' ' + str('F') + '\n')
    outputfile.write(str('Si') + ' ' + str('O') + '\n')
      
    #Reads in coordinates and writes it into outputfile without line spacing

    #For the Si atom, known now as atom 1
    for i in range(1,natoms[1] + 1):
       line =  inputfile.readline()
       outputfile.write(str(i) +' '+ str('1') +' ' + ' ' + line.strip() + '\n')
    #For the O atom, known now as atom 2
    print natoms[1],natoms[2]
    for j in np.arange(natoms[1]+1,natoms[1] + natoms[2]+1):
        line = inputfile.readline()
        outputfile.write(str(j) +' '+ str('2') +' ' + ' ' + line.strip() + '\n')
   
    #Add periodic boundary conditions to *.gen:
    outputfile.write(str(0.0000) + ' '+ str(0.0000)+ ' '+ str(0.0000) + '\n' + str(xlatt_line) + '\n' + str(ylatt_line) + '\n' + str(zlatt_line)) 
    
    inputfile.close()
    outputfile.close()
   
if __name__=='__main__':
    main() 
