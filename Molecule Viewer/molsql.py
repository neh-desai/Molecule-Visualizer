#Imports needed for using features of MolDisplay and sql lite
import MolDisplay; 
import os;
import sqlite3;

#Database class
class Database:
    def __init__(self, reset=False):
        #If reset it true delete the stated file so a fresh database can be created
        if (reset==True):
            os.remove( 'molecules.db')
        #Opening a database connection of the stated file and storing it as a class attribute
        self.connect = sqlite3.connect( 'molecules.db' );
    
    def create_tables(self):
        #Creating Table #1 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS Elements 
                 ( ELEMENT_NO  INTEGER NOT NULL,
                   ELEMENT_CODE  VARCHAR(3) NOT NULL,
                   ELEMENT_NAME  VARCHAR(32) NOT NULL,
                   COLOUR1  CHAR(6) NOT NULL,
                   COLOUR2  CHAR(6) NOT NULL,
                   COLOUR3  CHAR(6) NOT NULL, 
                   RADIUS   DECIMAL(3) NOT NULL,
                   PRIMARY KEY (ELEMENT_CODE));""");
        
        #Creating Table #2 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS Atoms
                 ( ATOM_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
                   ELEMENT_CODE   VARCHAR(3) NOT NULL,
                   X  DECIMAL(7,4) NOT NULL,
                   Y  DECIMAL(7,4) NOT NULL,
                   Z  DECIMAL(7,4) NOT NULL,
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""");

        #Creating Table #3 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS Bonds
                ( BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   A1  INTEGER NOT NULL,
                   A2  INTEGER NOT NULL,
                   EPAIRS INTEGER NOT NULL
                   )""")

        #Creating Table #4 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS Molecules
                 ( MOLECULE_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
                   NAME  TEXT UNIQUE NOT NULL
                   )""");
        
        #Creating Table #5 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom 
                 ( MOLECULE_ID INTEGER NOT NULL,
                   ATOM_ID INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""" );
        
        #Creating Table #6 with its attributes if it does not exist yet
        self.connect.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond 
                 ( MOLECULE_ID INTEGER NOT NULL,
                   BOND_ID INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, BOND_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (BOND_ID) REFERENCES Bonds);""");

    def __setitem__ (self, table, values):  
        #Setting a variable which holds the values tuple
        elementList = [values]; 
        #If the table we want to set values in is Elements than insert its coresponding values based on what is stored in elementList
        if (table=='Elements'):
            self.connect.executemany("""INSERT INTO Elements (ELEMENT_NO, ELEMENT_CODE, ELEMENT_NAME,
            COLOUR1, COLOUR2, COLOUR3, RADIUS) VALUES (?, ?, ?, ?, ?, ?, ?)""", elementList)
        #If the table we want to set values in is Atoms than insert its coresponding values based on what is stored in elementList
        if (table=='Atoms'):
            self.connect.executemany("""INSERT INTO Atoms (ATOM_ID, ELEMENT_CODE, X, Y, Z) VALUES (?, ?, ?, ?, ?)""", elementList)
        #If the table we want to set values in is Bonds than insert its coresponding values based on what is stored in elementList
        if (table=='Bonds'):
             self.connect.executemany("""INSERT INTO Bonds (BOND_ID, A1, A2, EPAIRS) VALUES (?, ?, ?, ?)""", elementList)  
        #If the table we want to set values in is Molecules than insert its coresponding values based on what is stored in elementList
        if (table=='Molecules'):
            self.connect.executemany("""INSERT INTO Molecules (MOLECULE_ID, NAME) VALUES (?, ?)""", elementList)
        #If the table we want to set values in is MoleculeAtom than insert its coresponding values based on what is stored in elementList
        if (table=='MoleculeAtom'):
            self.connect.executemany("""INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (?, ?)""", elementList)
        #If the table we want to set values in is MoleculeBond than insert its coresponding values based on what is stored in elementList
        if (table=='MoleculeBond'):
            self.connect.executemany("""INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (?, ?)""", elementList)
    
    def add_atom (self, molname, atom):
        #Adding the attributes of the atom object into the Atoms table with their coresponding type
        self.connect.execute("""INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES ('%s', %f, %f, %f)""" %(atom.element,atom.x, atom.y, atom.z))
        #Getting a cursor for our database and executing the SELECT command stated so we can get the Atom ID
        cursor = self.connect.cursor()
        cursor.execute("""SELECT Atoms.ATOM_ID FROM Atoms""")
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        #Getting another cursor for our database and executing the SELECT command stated to get the molecule ID associated with the name passed in
        cursor2 = self.connect.cursor()
        cursor2.execute("""SELECT Molecules.MOLECULE_ID FROM Molecules WHERE Molecules.NAME='%s' """%(molname))
        #Storing the information gotten from the table into the variable data2
        data2 = cursor2.fetchall()
        #Setting a variable equal to the molecule ID 
        idOfMol = data2[0][0]
        #Setting a variable equal to the length of all of the Atom ID's we got
        length = len(data)
        #Setting a variable equal to the latest Atom ID and since we data gotten from the table was a tuple I converted it into a integer
        idOfAtom = int (''.join(map(str,data[length-1])))
        #Adding an entry into the MoleculeAtom table with their associated molecule and atom ID's
        self.connect.execute("""INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (%d, %d)""" %(idOfMol,idOfAtom))

    def add_bond (self, molname, bond):
        #Adding the attributes of the bond object into the Bonds table with their coresponding type
        self.connect.execute("""INSERT INTO Bonds (A1, A2, EPAIRS) VALUES (%d, %d, %d)""" %(bond.a1,bond.a2, bond.epairs))
        #Getting a cursor for our database and executing the SELECT command stated so we can get the Bond ID
        cursor = self.connect.cursor()
        cursor.execute("""SELECT Bonds.BOND_ID FROM Bonds""")
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        #Setting a variable equal to the length of all of the Bond ID's we got
        length = len(data)
        #Getting another cursor for our database and executing the SELECT command stated to get the molecule ID associated with the name passed in
        cursor2 = self.connect.cursor()
        cursor2.execute("""SELECT Molecules.MOLECULE_ID FROM Molecules WHERE Molecules.NAME='%s' """%(molname))
        #Storing the information gotten from the table into the variable data2
        data2 = cursor2.fetchall()
        #Setting a variable equal to the molecule ID 
        idOfMol = data2[0][0]
        #Setting a variable equal to the latest Bond ID and since we data gotten from the table was a tuple I converted it into a integer
        idOfBond = int (''.join(map(str,data[length-1])))
        #Adding an entry into the MoleculeBond table with their associated molecule and bond ID's
        self.connect.execute("""INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (%d, %d)""" %(idOfMol,idOfBond))   

    def add_molecule (self, name, fp):
        #Creating a MolDisplay.Molecule object and calling its parse method with the fp parameter passed in
        newMol = MolDisplay.Molecule()
        newMol.parse(fp)
        #Adding an entry into the Molecules table NAME attribute with the name passed into the parameter
        self.connect.execute("""INSERT INTO Molecules (NAME) VALUES ('%s')"""%(name))   
        #Looping through the number of atoms and calling the add_atom function for each atom returned by get_atom
        for i in range (newMol.atom_no):
            self.add_atom(name,newMol.get_atom(i))
        #Looping through the number of bonds and calling the add_bond function for each bond returned by get_bond
        for j in range (newMol.bond_no):
            self.add_bond(name,newMol.get_bond(j))
    
    def load_mol (self, name):  
        #Creating a MolDisplay.Molecule object which this method returns
        newMol = MolDisplay.Molecule()
        #Getting a cursor for our database and executing the SELECT command stated so we can get all of the atoms associated with the named molecule passed in
        cursor = self.connect.cursor()
        cursor.execute("""SELECT * FROM Atoms, Molecules, MoleculeAtom WHERE Molecules.NAME = '%s' AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID AND MoleculeAtom.ATOM_ID=Atoms.ATOM_ID ORDER BY Atoms.ATOM_ID ASC""" %(name))
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        #Getting another cursor for our database and executing the SELECT command stated so we can get all of the bonds associated with the named molecule passed in
        cursor2 = self.connect.cursor()
        cursor2.execute("""SELECT * FROM Bonds, Molecules, MoleculeBond WHERE Molecules.NAME = '%s' AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID AND MoleculeBond.BOND_ID=Bonds.BOND_ID ORDER BY Bonds.BOND_ID ASC""" %(name))
        #Storing the information gotten from the table into the variable data2
        data2 = cursor2.fetchall()
        #Loop through the number of atoms gotten from the select statement
        for i in range (len(data)):
            #Call append_atom on the Molecule object with the parameters of the element and its x, y and z values which are typecasted to be floats
            newMol.append_atom(data[i][1], float(data[i][2]), float(data[i][3]), float(data[i][4]))
        #Loop through the number of bonds gotten from the select statement
        for j in range (len(data2)):
            #Call append_bond on the Molecule object with the parameters of A1, A2 and Epairs which are typecasted to be ints
            newMol.append_bond(int(data2[j][1]), int(data2[j][2]), int(data2[j][3]))
        #Return the Molecule object
        return newMol
    
    def radius (self):
        #Creating an empty dictonary which we will add information in and return
        dictonary = {}
        #Getting a cursor for our database and executing the SELECT command stated so we can link the Element Code values to the radius
        cursor = self.connect.cursor()
        cursor.execute("""SELECT Elements.ELEMENT_CODE, Elements.RADIUS FROM Elements""")
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        #Looping through the amount of information gotten
        for i in range (len(data)):
            #Adding onto the empty dictonary created by linking the element code and radius values
            dictonary[data[i][0]]=data[i][1]
        #Returning the radius dictonary created
        return dictonary

    def element_name (self):
        #Creating an empty dictonary which we will add information in and return
        dictonary = {}
        #Getting a cursor for our database and executing the SELECT command stated so we can link the Element Code values to the Element Name
        cursor = self.connect.cursor()
        cursor.execute("""SELECT Elements.ELEMENT_CODE, Elements.ELEMENT_NAME FROM Elements""")
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        #Looping through the amount of information gotten
        for i in range (len(data)):
            #Adding onto the empty dictonary created by linking the element code and name values
            dictonary[data[i][0]]=data[i][1]
        #Returning the element name dictonary created
        return dictonary
    
    def radial_gradients (self):
        #Getting a cursor for our database and executing the SELECT command stated so we can get the information needed from the Elements table to do the string sub
        cursor = self.connect.cursor()
        cursor.execute("""SELECT Elements.ELEMENT_NAME, Elements.COLOUR1, Elements.COLOUR2, Elements.COLOUR3 FROM Elements""")
        #Storing the information gotten from the table into the variable data
        data = cursor.fetchall()
        radialGradientSVG=""" 
        <radialGradient id="temp" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                <stop offset="0%" stop-color="#FFFFFF"/>
                <stop offset="50%" stop-color="#050505"/>
                <stop offset="100%" stop-color="#020202"/>
            </radialGradient>"""
        #Looping through the amount of elements gotten
        for i in range (len(data)):
            #Concatenating the string initialized above with the string constant below and string subbing them with the element name and the 3 different colours
            radialGradientSVG += """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>"""%(data[i][0], data[i][1], data[i][2], data[i][3]);
        #Returning the concatenations of the string
        return radialGradientSVG
    
    
