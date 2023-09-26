import molecule;
mol = molecule.molecule(); # create a new molecule object
# create 3 atoms
mol.append_atom( "O", 2.5369, -0.1550, 0.0000 );
mol.append_atom( "H", 3.0739, 0.1550, 0.0000 );
mol.append_atom( "H", 2.0000, 0.1550, 0.0000 );
# caution atom references in append_bond start at 1 NOT 0
mol.append_bond( 1, 2, 1 );
mol.append_bond( 1, 3, 1 );
for i in range(3):
    atom = mol.get_atom(i);
    print( atom.element, atom.x, atom.y, atom.z );
for i in range(2):
    bond = mol.get_bond(i);
    print( bond.a1, bond.a2, bond.epairs, bond.x1, bond.y1, bond.x2, bond.y2,bond.len, bond.dx, bond.dy );

radius = { 'H': 25,
'C': 40,
'O': 40,
'N': 40,
};
element_name = { 'H': 'grey',
'C': 'black',
'O': 'red',
'N': 'blue',
};
header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;

# class Atom:
#     def __init__(self, c_atom):
#         self.c_atom = c_atom;
#         self.z = c_atom.z; 

#     def __str__ (self):
#         return '''Element: %c X: %f Y: %f Z: %f''' % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z);
#         # xcord = self.c_atom.x * 100.0 + offsetx;
#         # ycord = self.c_atom.y * 100.0 + offsety;
#         # radCircle = radius[self.c_atom.element];
#         # colourCircle = element_name[self.c_atom.element];
#         # return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n'%(xcord, ycord,radCircle,colourCircle);

#     def svg(self):
#         xcord = self.c_atom.x * 100.0 + offsetx;
#         ycord = self.c_atom.y * 100.0 + offsety;
#         radCircle = radius[self.c_atom.element];
#         colourCircle = element_name[self.c_atom.element];
#         return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n'%(xcord, ycord,radCircle,colourCircle);
      
# class Bond:
#     def __init__(self, c_bond):
#          self.bond = c_bond;
#          self.z = c_bond.z;
    
#     def __str__ (self):
#         return '''A1: %d A2: %d Epairs: %d X1: %f Y1: %f X2: %f Y2: %f Length: %f dx: %f dy: %f ''' % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.len, self.bond.dx, self.bond.dy );

# class Bond:
#     def __init__(self, c_bond):
#          self.bond = c_bond;
#          self.z = c_bond.z;
    
#     def __str__ (self):
#         x1 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y1= (self.bond.y1 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         x2 = (self.bond.x1 * 100.0 + offsetx) + (self.bond.dy * 10.0 );
#         y2 = (self.bond.y1 * 100.0 + offsety) +  (self.bond.dx * 10.0); 
#         x3 = (self.bond.x2 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y3 = (self.bond.y2 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         x4 = (self.bond.x2 * 100.0 + offsetx) + (self.bond.dy * 10.0 );
#         y4 = (self.bond.y2 * 100.0 + offsety) +  (self.bond.dx * 10.0); 
#         return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n'%(x1,y1,x2,y2,x4,y4,x3,y3);
#         # return '''A1: %d A2: %d Epairs: %d X1: %f Y1: %f X2: %f Y2: %f Z: %f Length: %f dx: %f dy: %f ''' % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.z, self.bond.len, self.bond.dx, self.bond.dy );
    
#     def svg (self):
#         x1 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y1= (self.bond.y1 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         x2 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y2 = (self.bond.y1 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         x3 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y3 = (self.bond.y1 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         x4 = (self.bond.x1 * 100.0 + offsetx) - (self.bond.dy * 10.0 );
#         y4 = (self.bond.y1 * 100.0 + offsety) -  (self.bond.dx * 10.0); 
#         return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n'%(x1,y1,x2,y2,x3,y3,x4,y4);


# class Molecule (molecule.molecule) :
    # class mol (molecule.molecule):
        # def __str__ (self):
            # b1 = molecule.get_bond(0); 
            # b2 = molecule.get_bond(1);
            # a1 = molecule.get_atom(0);
            # a2 = molecule.get_atom(1);
            # a3 = molecule.get_atom(2);
            # return 'Atom1 %c %f %f  \n Atom2 %c %f %f\n Bond1 %d %d %d %c %f %f %f %f %f %f %f %f '%(a1.element, a1.x, a1.y, a2.element, a2.x, a2.y, b1.a1, b1.a2, b1.epairs, b1.atoms, b1.x1, b1.x2, b1.y1, b2.y2, b2.z, b2.len, b2.dx, b2.dy);
    

# atomTest = mol.get_atom(0);
# newAtom = Atom(atomTest);
# newAtom.svg();
# print(newAtom); 

# bondTest = mol.get_bond(0);
# newBond = Bond(bondTest);
# print(newBond);

# molTest = Molecule(mol);
# print(molTest);
