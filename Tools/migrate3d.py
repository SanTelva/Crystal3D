import sys
sys.path += ['..']
from draw2.nboio import *
from draw2.nbolib import *
from draw2._legacy.igorio import *

if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], 'input.igor3d output.nbo3d')
    __import__('_sitebuiltins').Quitter('','')(1) # exit(1)

angleA, angleB, angleG, a, b, c, primitiveCell = myInput(sys.argv[1])
nodes, bonds = igorToNBO((angleA, angleB, angleG, a, b, c, primitiveCell))
nboOutput(sys.argv[2], (angleA, angleB, angleG), a, b, c, nodes, bonds)
