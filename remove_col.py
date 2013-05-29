#Program to remove first column of an xyz file, as required to become a POSCAR file. NOTE: data here was already ordered so similar atoms are together
import os,sys
def main():
    inputfile = open('slab2_b.xyz', 'r')
    outputfile = open('slab2_b_001','w')
    
    x_array = []
    y_array = []
    z_array = []
    for line in inputfile.readlines():
        x_array = float(line.split()[1])
        y_array = float(line.split()[2])
        z_array = float(line.split()[3])
        print y_array
        outputfile.write(str(x_array) + ' ' + str(y_array) + ' ' + str(z_array) + '\n')
    inputfile.close()
    outputfile.close()
   
if __name__=='__main__':
    main()        
