#Program to extend POSCAR inputfile, a slab, in the x and y direction, and output the new file
import os,sys
def main():
    inputfile = open('POSCAR', 'r')
    outputfile = open('extend_POSCAR','w')
    #for line <= 2 in inputfile.readlines():
        #Want to skip over the first 2 lines of the POSCAR file
    for line > 2 in inputfile.readlines():
        x_lattice = float(line.split()[0]

    inputfile.close()
    outputfile.close()
if __name__=='__main__';
    main()
