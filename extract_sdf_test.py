from molecules_list import *

file_name = 'sdf_list.sdf'

file = open(file_name, 'tr')
file_as_string = file.read()
file_as_string = file_as_string.split('\n')

file = open(file_name, 'tr')
MolList = extract_molecules_list_from_sdf(file, 'Source')

index = 0

print('---------HEADER----------')
for row in MolList.mol_list[0].header_list:
    print('FILE:\t', file_as_string[index])
    index += 1
    print('LIST:\t', row)
# COUNTS LINE
print('FILE:\t', file_as_string[index])
index += 1
print('LIST:\t', end='  ')
for cell in MolList.mol_list[0].counts_line:
    print(cell, end='  ')
print()
# ATOM BLOCK
for row in MolList.mol_list[0].atom_block:
    print('FILE:\t', file_as_string[index])
    index += 1
    print('LIST:\t', end='  ')
    for cell in row:
        print(cell, end='  ')
    print()
# BOND BLOCK
for row in MolList.mol_list[0].bond_block:
    print('FILE:\t', file_as_string[index])
    index += 1
    print('LIST:\t', end='  ')
    for cell in row:
        print(int(cell), end='  ')
    print()
index += 1
# FIELDS



# print(MolList.mol_list[0].counts_line)
'''for row in MolList.mol_list[0].counts_line:
    print(row)
'''

print()

file.close()
    # print('lm dict:\n', MolList.mol_list[0].bond_block[})
# print('--------\n', lm.mol_list[0].bond_block)
# print('--------\n', lm.mol_list[0].atom_block)