import sys
sys.path += ['..']
from draw2.nboio import *
from draw2.nbolib import *
from draw2._legacy.igorio import *

if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], 'input.igor output.nbo')
    __import__('_sitebuiltins').Quitter('','')(1) # exit(1)

angle, a, b, primitiveCell = myInput(sys.argv[1])
nodes, bonds = igorToNBO((angle, a, b, primitiveCell))
nboOutput(sys.argv[2], angle, a, b, nodes, bonds)
