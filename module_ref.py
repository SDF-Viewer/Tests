import math
mol_gl, canv_gl = (None, None)
dict_of_aroma_bonds, type_bond_gl = ({}, 0)
three_valencies = set()
ERRORS_COUNTER = 0

"""
Unit for the depicting of molecule on the "canvas"
Global variable for this module:
  mol_gl  - variable for molecule, which should be depicted
 canv_gl – variable for "canvas"
 dict_of_aroma_bonds – dictionary of aromatic bonds
 type_bond_gl – type of the bond
 three_valencies – set of the atoms with no less than three bonds
"""


def for_circle(x, y, radius):
    return [x - radius, y - radius, x + radius, y + radius]


def into_center(center, scale0):
    """ shift a coordinate x to the centre (0) y to the centre(1), multiply size by scale0

    :param center: list with the coordinates of canvas centre
    :param scale0:Scale
    :return: None
    """
    try:
        global mol_gl
        summ, num, x_y_0 = ([0, 0], [0, 0], [0, 0])
        optimal_part = 0.85
        max_size, min_size = ([0, 0], [0, 0])

        for atom in mol_gl.atom_block:
            for i in 0, 1:
                summ[i] += atom[i]
                num[i] += 1
        for i in 0, 1:
            x_y_0[i] = summ[i] / num[i]
        for num_atom in range(len(mol_gl.atom_block)):
            atom = mol_gl.atom_block[num_atom]
            for i in 0, 1:
                current_size = atom[i]
                if (max_size[i] < current_size) or (num_atom == 0):
                    max_size[i] = current_size
                if (min_size[i] > current_size) or (num_atom == 0):
                    min_size[i] = current_size
        scale = [0, 0]
        delta = [0, 0]
        for i in 0, 1:
            k = (max_size[i] - min_size[i]) / 2
            delta[i] = (max_size[i] + min_size[i]) / 2
            scale[i] = center[i] * optimal_part / k
        scale = min(*scale) * scale0

        for num_atom in range(len(mol_gl.atom_block)):
            atom = mol_gl.atom_block[num_atom]
            for i in 0, 1:
                atom[i] -= delta[i]
                atom[i] *= scale
                atom[i] += center[i]
    except:
        send_error_msg()


def double_line(bond, ro=1):
    """ This function draws a double bond

    :param bond: depicted bond
    :param ro: space between lines
    :return: None
    """

    dist = 2
    double_bond = [[0 for i in range(4)] for j in [0, 1]]
    dist *= ro
    k_znam = bond[2] - bond[0]
    if k_znam == 0:
        almost_x_y = [dist, 0]
    else:
        k = (bond[3] - bond[1]) / k_znam
        if k == 0:
            almost_x_y = [0, dist]
        else:
            sign_k = k / abs(k)
            k *= k
            almost_x_y = [dist / math.sqrt(1 / k + 1), - dist / math.sqrt(k + 1) * sign_k]
    for bond_i in [0, 1]:
        for coord_i in [0, 1, 2, 3]:
            double_bond[bond_i][coord_i] = (2 * bond_i - 1) * almost_x_y[coord_i % 2] + bond[coord_i]
    for i in [0, 1]:
        canv_gl.create_line(*double_bond[i], width=2, tag=str(bond[4]))


def draw_bond(num_atom1, num_atom2, type_bond):
    """ This function draws bond

    :param num_atom1: first atom
    :param num_atom2: second atom
    :param type_bond: type of the bond
    :return: None
    """
    ro = 3
    atom1 = mol_gl.atom_block[int(num_atom1) - 1][:2]
    atom2 = mol_gl.atom_block[int(num_atom2) - 1][:2]
    bond = []
    bond.extend(atom1)
    bond.extend(atom2)
    bond.append(type_bond)
    if type_bond == 1:
        canv_gl.create_line(*bond[:4], width=2, tag=str(type_bond))
    elif type_bond == 2:
        double_line(bond)
    elif type_bond == 3:
        double_line(bond, ro=ro)
        canv_gl.create_line(*bond[:4], width=2, tag=str(type_bond))
    else:
        canv_gl.create_line(*bond[:4], width=2, tag=str(type_bond), fill="red")


def draw_mol(mol, canv0, scale=1):
    """ This function depicts a molecule

    :param mol: molecule
    :param canv0: canvas
    :param scale: scale
    :return: None
    """
    try:
        " This function renews the global variable and sets value of argument on default"
        global mol_gl, canv_gl, dict_of_aroma_bonds, type_bond_gl, three_valencies
        dict_of_aroma_bonds, type_bond_gl = ({}, 0)
        three_valencies = set()
        import copy
        mol_gl = copy.deepcopy(mol)
        canv_gl = canv0
        ''' This function gets height and width of the canvas – defines corrections
            for transfer of molecule to the centre of the canvas'''
        height = canv0.winfo_reqheight()
        width = canv0.winfo_reqwidth()
        center = [width / 2, height / 2]
        " changes the parameter of “scroll region”  with the increase of the scale"
        difference = (scale - 1) / 2
        delta_width = width * difference
        delta_height = height * difference
        canv_gl.config(scrollregion=(0 - delta_width, 0 - delta_height, width + delta_width, height + delta_height))
        " transfer of the atom coordinates to the centre and scaling of the bonds length"
        into_center(center, scale0=scale)
        """
        filtration of the bonds in aromatic and others
        if the bond is aromatic, the bond will be added into the dictionary
        if the bond is not aromatic, the bond will be drawn.
        """

        for num_bond in range(len(mol_gl.bond_block)):
            bond = mol_gl.bond_block[num_bond][:3]
            if bond[2] == 4:
                bond[2] = 1
                into_aroma_dict(*bond)
            else:
                draw_bond(*bond)
        " draws an aromatic bond"
        create_sp_trees()
        for atom in dict_of_aroma_bonds:
            for near_atom in dict_of_aroma_bonds[atom]:
                bond = [atom, near_atom, dict_of_aroma_bonds[atom][near_atom]]
                draw_bond(*bond)
        " writes names of the atoms"
        for atom in mol_gl.atom_block:
            x_y = atom[:2]
            x_y_r = for_circle(*x_y, radius=7)
            canv_gl.create_oval(*x_y_r, fill="lightyellow", outline="lightyellow")
            name = atom[3]
            color_name = "darkgrey" if name == "C" else "red"
            canv_gl.create_text(*x_y, text=name, font="Verdana 12", fill=color_name)
    except:
        send_error_msg()


def into_aroma_dict(start, finish, weight):
    """ This function adds bonds to the list of aromatic bonds

    :param start: one atom
    :param finish: another atom
    :param weight: their bond's type
    :return: None
    """
    global dict_of_aroma_bonds
    if start not in dict_of_aroma_bonds:
        dict_of_aroma_bonds[start] = {finish: weight}
    else:
        dict_of_aroma_bonds[start][finish] = weight
    if finish not in dict_of_aroma_bonds:
        dict_of_aroma_bonds[finish] = {start: weight}
    else:
        dict_of_aroma_bonds[finish][start] = weight


def create_sp_trees():
    """ This function finds aromatic rings

    :return: None
    """
    global three_valencies, type_bond_gl, dict_of_aroma_bonds
    " using the algorithm of depth-first traversal, we change the type from aromatic bond to sigma-bond or pi-bond"
    for atom in dict_of_aroma_bonds:
        if atom not in three_valencies:
            type_bond_gl = 0
            dfs_aroma(atom)


def dfs_aroma(atom):
    """ This function changes aromatic bond to the single bond or double bond

    :param atom: atom
    :return: None
    """
    global three_valencies, type_bond_gl, dict_of_aroma_bonds
    " using the algorithm of depth-first traversal, we change the type from aromatic bond to sigma-bond or pi-bond"
    three_valencies.add(atom)
    last_atom = None
    for near_atom in dict_of_aroma_bonds[atom]:
        last_atom = near_atom
        if near_atom not in three_valencies:
            type_bond_l = 2 - type_bond_gl % 2
            dict_of_aroma_bonds[atom][near_atom] = type_bond_l
            dict_of_aroma_bonds[near_atom][atom] = type_bond_l
            type_bond_gl += 1
            last_atom = dfs_aroma(near_atom)
    return last_atom


def send_error_msg():
    global ERRORS_COUNTER
    ERRORS_COUNTER += 1
    if ERRORS_COUNTER < 2:
        import tkinter.messagebox
        tkinter.messagebox.showerror(title='Сообщение', message='Информация о молекуле некорректна')
    else:
        pass