#include "mol.h"

void atomset(atom * atom, char element[3], double * x, double * y, double * z) {
  //Copies the element value and the values of x, y and z into atom
  strcpy(atom -> element, element);
  atom -> x = * x;
  atom -> y = * y;
  atom -> z = * z;
}

void atomget(atom * atom, char element[3], double * x, double * y, double * z) {
  //Copies the values stored in atom to the corresponding parameters
  * x = atom -> x;
  * y = atom -> y;
  * z = atom -> z;
  strcpy(element, atom -> element);
}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
  //Copies the values pointed to by a1, a2, atoms and epairs into the proper bond struct
  bond->a1=*a1;
  bond->a2=*a2;
  bond->epairs=*epairs;
  bond->atoms=*atoms;
  compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
  //Copies the values stored in bond to the corresponding parameters
  *epairs=bond->epairs;
  *a1=bond->a1;
  *a2=bond->a2;
  *atoms=bond->atoms;
}

void compute_coords( bond *bond ){
  //Stores x1,y1,x2 and y2 into the proper bond structure variable
  bond->x1=bond->atoms[bond->a1].x;
  bond->x2=bond->atoms[bond->a2].x;
  bond->y1=bond->atoms[bond->a1].y;
  bond->y2=bond->atoms[bond->a2].y;
  //Calcultes the z value and stores it in the proper bond structure variable
  bond->z=(bond->atoms[bond->a1].z + bond->atoms[bond->a2].z)/2;
  //Calcultes the length and stores it in the proper bond structure variable
  bond->len = sqrt((bond->x2-bond->x1) *(bond->x2-bond->x1) + (bond->y2-bond->y1)*(bond->y2-bond->y1));
  //Calcultes the distance between x and y and stores it in the proper bond structure variable
  bond->dx=(bond->x2 - bond->x1)/bond->len; 
  bond->dy=(bond->y2 - bond->y1)/bond->len; 
}

molecule * molmalloc(unsigned short atom_max, unsigned short bond_max) {
  //Temp molecule pointer created which is the value returned by this function
  molecule * molptr = malloc(sizeof(molecule));
  //Error checking
  if (molptr == NULL) {
    return NULL;
  }
  //Set the maximum values to the ones being passed in by the parameters
  molptr -> atom_max = atom_max;
  molptr -> bond_max = bond_max;
  //Settings atom number and bond number to 0 
  molptr -> atom_no = 0;
  molptr -> bond_no = 0;
  //Enough memory is allocated to the atoms array
  molptr -> atoms = malloc(sizeof(struct atom) * atom_max);
  //Error checking
  if (molptr -> atoms == NULL) {
    return NULL;
  }
  //Enough memory is allocated to the bonds array
  molptr -> bonds = malloc(sizeof(struct bond) * bond_max);
  //Error Checking
  if (molptr -> bonds == NULL) {
    return NULL;
  }
  //Enough memeory is allocated to the double pointer atoms_ptrs
  molptr -> atom_ptrs = (atom ** ) malloc(sizeof(struct atom * ) * atom_max);
  //Error checking
  if (molptr -> atom_ptrs == NULL) {
    return NULL;
  }
  //Enough memory is allocated to the double pointer bond_ptrs
  molptr -> bond_ptrs = (bond ** ) malloc(sizeof(struct bond * ) * bond_max);
  //Error checking
  if (molptr -> bond_ptrs == NULL) {
    return NULL;
  }
  return molptr;
}

molecule * molcopy(molecule * src) {
  //Variable of type molecule created to get passed in parameters
  molecule * val = molmalloc(src -> atom_max, src -> bond_max);
  //Loop that goes until the number of atoms in the array and appends it to the variable created above
  for (int i = 0; i < src -> atom_no; i++) {
    molappend_atom(val, & src -> atoms[i]);
  }
  //Loop that goes until the number of bonds and appends it to the variable created above
  for (int i = 0; i < src -> bond_no; i++) {
    molappend_bond(val, & src -> bonds[i]);
  }
  //val which holds the copied elements is returned
  return val;
}

void molfree(molecule * ptr) {
  //1 free for everthing we have allocated in the program
  free(ptr -> atoms);
  free(ptr -> atom_ptrs);
  free(ptr -> bonds);
  free(ptr -> bond_ptrs);
  free(ptr);
}

void molappend_atom(molecule * molecule, atom * atom) {
  if (molecule -> atom_max == 0 && molecule -> atom_no == molecule -> atom_max) {
    //Increment atom max by 1
    molecule -> atom_max += 1;
    //Resize the atoms array since we have increased atom max
    molecule -> atoms = realloc(molecule -> atoms, sizeof(struct atom) * (molecule -> atom_max));
    //Resize the double pointer since we have increased atom max
    molecule -> atom_ptrs = realloc(molecule -> atom_ptrs, sizeof(struct atom * ) * (molecule -> atom_max));
  } else if (molecule -> atom_no == molecule -> atom_max) {
    //Double atom max 
    molecule -> atom_max *= 2;
    //Resize the atoms array since we have increased atom max
    molecule -> atoms = realloc(molecule -> atoms, sizeof(struct atom) * (molecule -> atom_max));
    //Resize the double pointer since we have increased atom max
    molecule -> atom_ptrs = realloc(molecule -> atom_ptrs, sizeof(struct atom * ) * (molecule -> atom_max));
  }
  //Reorganizes the atom arrays so that they point to their correct locations
  for (int i = 0; i < molecule -> atom_no; i++) {
    molecule -> atom_ptrs[i] = & molecule -> atoms[i];
  }
  //Statements that assign the corresponding values of the atoms to the according atom arrays
  molecule -> atoms[molecule -> atom_no] = * atom;
  molecule -> atom_ptrs[molecule -> atom_no] = & molecule -> atoms[molecule -> atom_no];
  //Increment atom no as another element has been added
  molecule -> atom_no += 1;
}

void molappend_bond(molecule * molecule, bond * bond) {
  if (molecule -> bond_max == 0 && molecule -> bond_no == molecule -> bond_max) {
    //Increment bond max by 1
    molecule -> bond_max += 1;
    //Resize the bonds array since we have increased bond max
    molecule -> bonds = realloc(molecule -> bonds, sizeof(struct bond) * (molecule -> bond_max));
    //Resize the double pointer since we have increased bond max
    molecule -> bond_ptrs = realloc(molecule -> bond_ptrs, sizeof(struct bond * ) * (molecule -> bond_max));
  } else if (molecule -> bond_no == molecule -> bond_max) {
    //Double bond max
    molecule -> bond_max *= 2;
    //Resize the bonds array since we have increased bond max
    molecule -> bonds = realloc(molecule -> bonds, sizeof(struct bond) * (molecule -> bond_max));
    //Resize the double pointer since we have increased bond max
    molecule -> bond_ptrs = realloc(molecule -> bond_ptrs, sizeof(struct bond * ) * (molecule -> bond_max));
  }
  //Reorganizes the bond arrays so that they point to their correct locations
  for (int i = 0; i < molecule -> bond_no; i++) {
    molecule -> bond_ptrs[i] = & molecule -> bonds[i];
  }
  //Statements that assign the corresponding values of the bonds to the according bond arrays
  molecule -> bonds[molecule -> bond_no] = * bond;
  molecule -> bond_ptrs[molecule -> bond_no] = & molecule -> bonds[molecule -> bond_no];
  //Increment bond number as another one has been added
  molecule -> bond_no += 1;
}

int atom_comp(const void * a, const void * b) {
  //Creating temporary double pointers to be used and casting them
  struct atom ** aptr, ** bptr;
  aptr = (struct atom ** ) a;
  bptr = (struct atom ** ) b;
  //The z values are compared and according to the comparison the proper value is returned
  if (( * aptr) -> z < ( * bptr) -> z) {
    return -1;
  } else if (( * aptr) -> z == ( * bptr) -> z) {
    return 0;
  } else {
    return 1;
  }
}

int bond_comp(const void * a, const void * b) {
  //Creating temporary double pointers to be used and casting them
  struct bond ** aptr, ** bptr;
  aptr = (struct bond ** ) a;
  bptr = (struct bond ** ) b;
  //The average z value of the 2 atoms in the bond are stored in these variables 
  double avgAtom1 = ( * aptr) -> z;
  double avgAtom2 = ( * bptr) -> z;
  //The average z values of the atoms are compared and the proper value is returned
  if (avgAtom1 < avgAtom2) {
    return -1;
  } else if (avgAtom1 == avgAtom2) {
    return 0;
  } else {
    return 1;
  }
}

void molsort(molecule * molecule) {
  //Calls their according qsort functions for the sort to be done
  qsort(molecule -> atom_ptrs, molecule -> atom_no, sizeof(struct atom * ), &atom_comp);
  qsort(molecule -> bond_ptrs, molecule -> bond_no, sizeof(struct bond * ), &bond_comp);
}

void xrotation(xform_matrix xform_matrix, unsigned short deg) {
  //Converting the degrees passed into the parameters into radians
  double radian = deg * (PI / 180);
  //Setting the matrix to the x rotation matrix values
  xform_matrix[0][0] = 1;
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = 0;
  xform_matrix[1][0] = 0;
  xform_matrix[1][1] = cos(radian);
  xform_matrix[1][2] = -sin(radian);
  xform_matrix[2][0] = 0;
  xform_matrix[2][1] = sin(radian);
  xform_matrix[2][2] = cos(radian);
}

void yrotation(xform_matrix xform_matrix, unsigned short deg) {
  //Converting the degrees passed into the parameters into radians
  double radian = deg * (PI / 180);
  //Setting the matrix to the y rotation matrix values
  xform_matrix[0][0] = cos(radian);
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = sin(radian);
  xform_matrix[1][0] = 0;
  xform_matrix[1][1] = 1;
  xform_matrix[1][2] = 0;
  xform_matrix[2][0] = -sin(radian);
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = cos(radian);
}

void zrotation(xform_matrix xform_matrix, unsigned short deg) {
  //Converting the degrees passed into the parameters into radians
  double radian = deg * (PI / 180);
  //Setting the matrix to the z rotation matrix values
  xform_matrix[0][0] = cos(radian);
  xform_matrix[0][1] = -sin(radian);
  xform_matrix[0][2] = 0;
  xform_matrix[1][0] = sin(radian);
  xform_matrix[1][1] = cos(radian);
  xform_matrix[1][2] = 0;
  xform_matrix[2][0] = 0;
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = 1;
}

void mol_xform(molecule * molecule, xform_matrix matrix) {
  //Temporary double values created to hold the x, y and z values 
  double x;
  double y;
  double z;
  //Loop that goes through the number of atoms
  for (int i = 0; i < molecule -> atom_no; i++) {
    //Setting the x, y and z values into the temp variables so they do not get overwritten as the loop progresses
    x = molecule -> atoms[i].x;
    y = molecule -> atoms[i].y;
    z = molecule -> atoms[i].z;
    //Matrix multiplication is done on the coresponding values to get the final rotation matrix
    molecule -> atoms[i].x = (matrix[0][0] * x) + (matrix[0][1] * y) + (matrix[0][2] * z);
    molecule -> atoms[i].y = (matrix[1][0] * x) + (matrix[1][1] * y) + (matrix[1][2] * z);
    molecule -> atoms[i].z = (matrix[2][0] * x) + (matrix[2][1] * y) + (matrix[2][2] * z);
  }
  //Applying the compute coords function to the bond elements
  for (int j=0; j<molecule->bond_no;j++){
    compute_coords(&molecule->bonds[j]);
  }
}
