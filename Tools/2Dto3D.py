import sys
sys.path += ['..']
from draw2.nboio import *
from draw2.nbolib import *

if len(sys.argv) < 3:
    print('Usage:', 'input.nbo output.nbo3d')
    __import__('_sitebuiltins').Quitter('','')(1) # exit(1)

angle, a, b, nodes, bonds = nboInput(sys.argv[1])
for node in nodes:
    node.z = 0.5
    newBond = Bond(len(bonds.data) + 1, node.num, node.num, 0, 0, 1)
    node.bonds.append(newBond)
    bonds.append(newBond)
    
for bond in bonds:
    if bond.shiftZ is None:
        bond.shiftZ = 0

nboOutput(sys.argv[2], (90, angle, 90), a, b, (a + b) / 2, nodes, bonds)