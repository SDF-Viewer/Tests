#from module_ref import*
from UnitTestFunction import*

b = ListOfTestingExpressionsAndExpectedResults("module_ref.into_center(VAR)", ["[120, 30], 10_[1, 1, 1, 1, 1, 1, 1, 1, 1]",\
                                                                 "[0, 30], 10_[1, 1, 1, 1, 1, 1, 1, 1, 1]",\
                                                                 "[120, 0], 10_[1, 1, 1, 1, 1, 1, 1, 1, 1]",\
                                                                 "[120, 30], 1_[1, 1, 1, 1, 1, 1, 1, 1, 1]"])
print(b)
s = """import molecules_list
file = open('sdf_list.SDF', 'tr')
lm = molecules_list.extract_molecules_list_from_sdf(file, 'Source')
file.close()
module_ref.mol_gl=lm.mol_list[29]
"""
UnitTestFunction(module="module_ref",exec_code=s, TestingExpressionsAndExpectedResults=b)