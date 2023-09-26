#Importing our c library so we can access its features
import molecule;

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;


class Atom:
    #Constructor with the atom struct as an argument
    def __init__(self, c_atom):
        #Initialzing the variables
        self.c_atom = c_atom;
        self.z = c_atom.z; 

    def __str__ (self):
        #Returning values of the wrapped atom
        return '''Element: %c X: %f Y: %f Z: %f''' % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z);

    def svg (self):
        #Information to be returned is calculated using the description given in the assignment
        xcord = self.c_atom.x * 100.0 + offsetx;
        ycord = self.c_atom.y * 100.0 + offsety;
        if self.c_atom.element in radius:
            radCircle = radius[self.c_atom.element];
            colourCircle = element_name[self.c_atom.element];
        else:
            colourCircle = "temp"; 
            radCircle = 25;
        #Returning the information calculated above
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n'%(xcord, ycord,radCircle,colourCircle);

class Bond:
    #Constructor with the bond struct as an argument
    def __init__(self, c_bond):
         #Initialzing the variables
         self.bond = c_bond;
         self.z = c_bond.z;
    
    def __str__ (self):
        #Returning values of the wrapped atom
        return '''A1: %d A2: %d Epairs: %d X1: %f Y1: %f X2: %f Y2: %f Z: %f Length: %f dx: %f dy: %f ''' % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.z, self.bond.len, self.bond.dx, self.bond.dy );
    
    def svg (self):
        #Calculating the rectangular line to be drawn from one atom to another
        #First set of points
        x1 = (self.bond.x1 * 100.0 + offsetx) + (self.bond.dy * 10.0 );
        y1 =  (self.bond.y1  * 100.0 + offsety) -  (self.bond.dx * 10.0); 
        #Second set of points
        x2 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
        y2 = (self.bond.y1 * 100.0 + offsety) +  (self.bond.dx * 10.0); 
        #Third set of points
        x3 = (self.bond.x2 * 100.0 + offsetx) + (self.bond.dy * 10.0 );
        y3 = (self.bond.y2 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
        #Fourth set of points
        x4 = (self.bond.x2 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
        y4 = (self.bond.y2 * 100.0 + offsety) +  (self.bond.dx * 10.0); 
        #Returning the points of the 4 corners of the rectangle
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n'%(x1,y1,x2,y2,x4,y4,x3,y3);

class Molecule (molecule.molecule):
    def __str__ (self):
        #Loop that goes through the atoms and prints them out by adding them onto the string
        String1 = "Atoms: \n";
        for i in range (self.atom_no):
            atomnew = self.get_atom(i);
            atom = Atom(atomnew);
            String1+= (atom.__str__()+"\n")
        #Loop that goes through the bonds and prints them out by adding them onto the string
        String1+="Bonds: \n"
        for j in range (self.bond_no):
            bondnew = self.get_bond(j)
            bond = Bond (bondnew)
            String1+= (bond.__str__()+"\n")
        #Returning the string that holds the atoms and bonds 
        return String1; 
        
    def svg (self):
        #String initialized to the header defined above
        String = header; 
        #Varibles declared that are used inside the method
        val1 = 0
        val2 = 0
        #While loop that goes through the atoms and bonds 
        while (val1!=self.atom_no and val2!=self.bond_no):
            #Variables that get and store the atom
            atomnew = self.get_atom(val1);
            atom = Atom(atomnew);
            #Variables that get and store the bond
            bondnew = self.get_bond(val2)
            bond = Bond (bondnew)
            #Using the sorting algorithm talked about on the assignment to get the smallest z value
            if (atom.z < bond.z):
                String += atom.svg()
                val1 += 1
            else:
                String += bond.svg()
                val2 += 1
        #Loop that goes through the atoms and bonds we have left 
        if (val1 == self.atom_no):
            for i in range (val2,self.bond_no):
                bondnew = self.get_bond(i)
                bond = Bond (bondnew)
                String += bond.svg()
        else:
            for j in range (val1, self.atom_no):
                atomnew = self.get_atom(j)
                atom = Atom (atomnew)
                String += atom.svg()
        #Add the footer defined above to the String and return it
        String += footer 
        return String
    
    def parse (self,file):
        #Start reading the lines from the file passsed in
        info = file.readlines()
        #Skip the first 4 lines and start reading since thats where the information is
        Line = info[3]
        #Remove the spaces and store them in their according indices 
        moreInfo = Line.split()
        #Store the atom and bond numbers which come one after another
        atomNum = int(moreInfo[0])
        bondNum = int (moreInfo[1])
        #Variable that holds when to stop reading the atoms
        stopAtomRead = atomNum + 4; 
        #Loop for all the atoms we have
        for i in range (4,stopAtomRead):
            #Get the information from the lines
            Line = info[i]
            #Remove the spaces and store them in their according indicies
            moreInfo = Line.split()
            #Append the atom information gotten accordingly
            self.append_atom(moreInfo[3], float(moreInfo[0]), float(moreInfo[1]),float(moreInfo[2]))
            # print(moreInfo[3],float(moreInfo[0]), float(moreInfo[1]),float(moreInfo[2]))
        #Loop for all the bonds we have
        for j in range (stopAtomRead, stopAtomRead + bondNum):
            #Get the information from the lines
            Line = info[j]
            #Remove the spaces and store them in their according indicies
            moreInfo = Line.split()
            #Append the bond information gotten accordingly
            self.append_bond(int(moreInfo[0]) -1, int(moreInfo[1]) -1,int(moreInfo[2]))
            # print(int(moreInfo[0]), int(moreInfo[1]), int(moreInfo[2]))
        #close the file being read from
        file.close()