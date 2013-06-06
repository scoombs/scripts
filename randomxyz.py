#!usr/bin/env python
#This code generates a random xyz file. This will be used to check g(r) functions in I.S.A.A.C.S --- expecting to see a plot of a straight line.
import random,sys,os

def main():
   #Allow the user to input natoms
    try: 
        program = sys.argv[0] #Gives filename
        natoms = int(sys.argv[1])
        #nsteps = int(sys.argv[2])
    except IndexError:
        #Tell user what is needed
        print '\nusage: '+program+' natoms (where natoms is an integer)\n'
        #Exit program cleanly
        sys.exit(0)
       
    outfile = open('randomcoordinates.xyz','w')
    #Generates 3 lists for floats between 0 and 100 of length natoms
    x = [random.uniform(0,100) for _ in range(0,natoms)] 
    y = [random.uniform(0,100) for _ in range(0,natoms)]
    z = [random.uniform(0,100) for _ in range(0,natoms)]
    
    atomtype = 'Si'
    #Format of the written xyz file :
    outfile.write(str(natoms) + '\n'+ '\n')
    for i in range(natoms):
        outfile.write(str(atomtype) + ' ' +str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + '\n' )

    outfile.close()

if __name__=='__main__':
   main()
