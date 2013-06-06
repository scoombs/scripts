#This code generates a random xyz file. This will be used to check g(r) functions in I.S.A.A.C.S --- expecting to see a plot of a straight line.
import random,sys,os

def main():

    outfile = open('randomcoordinates.xyz','w')
    #Generates 3 lists for integers between 0 and 100 of length 90
    x = random.sample(range(100),90)
    y = random.sample(range(100),90)
    z = random.sample(range(100),90)

    atomtype = 'Si'

    for i in range(90):
        outfile.write(str(atomtype) + ' ' +str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + '\n' )

    outfile.close()

if __name__=='__main__':
   main()
