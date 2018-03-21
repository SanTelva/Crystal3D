from draw2.nboio import *
from draw2.nbolib import *

def myInput(filename):
    inputData = nboInput(filename)
    if len(inputData) == 8: # Is 3D
        angleA, angleB, angleG, a, b, c, nodes, bonds = inputData
        return nboToIGOR(nodes, bonds, (angleA, angleB, angleG), a, b, c)
    angle, a, b, nodes, bonds = inputData
    return nboToIGOR(nodes, bonds, angle, a, b)

def myOutput(filename, primitiveCell):
    if type(primitiveCell[3]) == type([]) or type(primitiveCell[3]) == type(()): # Is 2D
        angle, a, b, _, _ = primitiveCell
        nodes, bonds = igorToNBO(primitiveCell)
        nboOutput(filename, angle, a, b, nodes, bonds)
    else:
        angleA, angleB, angleG, a, b, c = primitiveCell
        nodes, bonds = igorToNBO(primitiveCell)
        nboOutput(filename, angle, a, b, c, nodes, bonds)