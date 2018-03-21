from math import *
from draw2.maths import *
from draw2.nbolib import *
from copy import copy

def fracToAbsolute3D(xf, yf, zf, angleA, angleB, angleG, a, b, c):
    '''
    fracToAbsolute(xf, yf, zf, angleA, angleB, angleG, a, b, c) -> x, y, z
    Converts frac coords to absolute coords.
    "xf", "yf", "zf" are frac coords.
    "angleA" is angle between X and Z cell sides.
    "angleB" is angle between axis Y and X cell sides.
    "angleG" is angle between Y and Z cell sides.
    "a", "b", "c" are lengths of primitive cell sides
    "x", "y", "z" are absolute coords.
    '''
    #print("xf, yf, zf:", xf, yf, zf, "angleA, angleB, angleG, a, b, c:", angleA, angleB, angleG, a, b, c)
    #x = round(xf * a + cos(angleB) * yf * b + cos(angleA) * zf * c)
    kx = cos(angleA)
    ky = (cos(angleG) - kx * cos(angleB)) / sin(angleB)
    #y = round(yf * sin(angleB) * b + zf * c * ky)
    #z = round(zf *  * c)
    vect_i = Vector(1, 0, 0)
    vect_j = Vector(cos(angleB), sin(angleB), 0)
    vect_k = Vector(kx, ky, sqrt(1 - kx ** 2 - ky ** 2))  
    #print(vect_i * xf * a + vect_j * yf * b + vect_k * zf * c)
    return (round(coordinate) for coordinate in tuple(vect_i * xf * a + vect_j * yf * b + vect_k * zf * c))


def getPoints3D(angleA, angleB, angleG, a, b, c, PrimitiveCell, field_width, field_height):
    '''
    getPoints(angle, a, b, primitiveCell, field_width, field_height) -> Nodes, Bonds, PCs
    "angleA" is angle between X and Z cell sides.
    "angleB" is angle between axis Y and X cell sides.
    "angleG" is angle between Y and Z cell sides.
    "a", "b" and "c" are lengths of primitive cell sides.
    "field_width" and "field_height" are size of field.
    "primitiveCell" is list, containing nodes. Each node is list [num, x, y, z,  [bonds]] where:
    "num" is number of node (numeration starts from 1)
    "x", "y", "z" are coords of node, relative to primitive cell.
    Each bond is list [shiftX, shiftY, shiftZ, num] where:
    "shiftX", "shiftY", "shiftZ" are shifts in primitive cells to other node.
    "num" is number of other node.
    '''
    
    # German comment from previous version:
    # Check diesen Ungleichungen:
    # x: -a <= x <= field_width + a
    # y: -b <= y <= field_height + b
    
    Nodes = []
    Bonds = []
    readyNodes, readyBonds = igorToNBO([angleA, angleB, angleG, a, b, c, PrimitiveCell])
    PCs = []
    zf = -4
    #outOfImagination_Z = False
    while zf < 0:
        yf = -1
        outOfImagination_Y = False
        while not outOfImagination_Y:
            
    #        print("outOfImagination_Y:", outOfImagination_Y)
            xf = -5
            outOfImagination_X = False
            while not outOfImagination_X:
                
                PCs.append([[xf, yf, zf, xf, yf + 1, zf], [xf, yf, zf, xf + 1, yf, zf], [xf, yf, zf, xf, yf, zf + 1]])
                
                x, y, z = fracToAbsolute(xf, yf, zf, angleA, angleB, angleG, a, b, c) # Check whether out of field
                #print("x, y, z:", x, y, z, "field_width + a:", field_width + a)
                if x >= 3:
                #if x >= int(field_width + a):
                    outOfImagination_X = True
                xf += 1
    #            print("outOfImagination_X:", outOfImagination_X)
                for node in PrimitiveCell: # Set array if nodes
                    #print(node)
                    xf0 = node[1] + xf
                    yf0 = node[2] + yf
                    zf0 = node[3] + zf
                    Nodes.append((xf0, yf0, zf0))
                    
                    # Set array of bonds
                    for bond in node[4:]: # bond: [shiftX, shiftY, nodeNumber (in PrimitiveCell[,1])]
                        #print(bond)
                        xf1 = PrimitiveCell[bond[3] - 1][1] + xf + bond[0]
                        yf1 = PrimitiveCell[bond[3] - 1][2] + yf + bond[1]
                        zf1 = PrimitiveCell[bond[3] - 1][2] + zf + bond[2]
                        Bonds.append([xf0, yf0, zf0, xf1, yf1, zf1])
            if y >= 3:
            #if y >= field_height + b:
                outOfImagination_Y = True
            yf += 1
        zf += 1
    return Nodes, Bonds, PCs, readyNodes, readyBonds

def fracToAbsolute2D(xf, yf, angle, a, b):
    '''
    fracToAbsolute(xf, yf, angle, a, b) -> x, y
    Converts frac coords to absolute coords.
    "xf" and "yf" are frac coords.
    "angle" is angle between primitive cell sides.
    "a" and "b" are lengths of primitive cell sides
    "x" and "y" are absolute coords.
    '''
    # print("xf, yf:", xf, yf, "angle, a, b:", angle, a, b)
    x = int(xf * a + cos(angle) * yf * b)
    y = int((yf * sin(angle)) * b)
    return x, y


def getPoints2D(angle, a, b, PrimitiveCell, field_width, field_height):
    '''
    getPoints(angle, a, b, primitiveCell, field_width, field_height) -> Nodes, Bonds, PCs
    "angle" is angle between primitive cell sides.
    "a" and "b" are lengths of primitive cell sides.
    "field_width" and "field_height" are size of field.
    "primitiveCell" is list, containing nodes. Each node is list [num, x, y, [bonds]] where:
    "num" is number of node (numeration starts from 1)
    "x" and "y" are coords of node, relative to primitive cell.
    Each bond is list [shiftX, shiftY, num] where:
    "shiftX" and "shiftY" are shifts in primitive cells to other node.
    "num" is number of other node.
    '''
    
    # German comment from previous version:
    # Check diesen Ungleichungen:
    # x: -a <= x <= field_width + a
    # y: -b <= y <= field_height + b
    
    Nodes = []
    Bonds = []
    PCs = []
    yf = -1
    outOfImagination_Y = False
    while not outOfImagination_Y:
        xf = -5
        outOfImagination_X = False
        while not outOfImagination_X:
            PCs.append([[xf, yf, xf, yf + 1], [xf, yf, xf + 1, yf]])
            x, y = fracToAbsolute(xf, yf, angle, a, b)
            if x >= int(field_width + a):
                outOfImagination_X = True
            xf += 1
            for node in PrimitiveCell:
                # print(node)
                xf0 = node[1] + xf
                yf0 = node[2] + yf
                Nodes.append((xf0, yf0))
                for bond in node[3:]:
                    xf1 = PrimitiveCell[bond[2] - 1][1] + xf + bond[0]
                    yf1 = PrimitiveCell[bond[2] - 1][2] + yf + bond[1]
                    Bonds.append([xf0, yf0, xf1, yf1])
        
        if y >= field_height + b:
            outOfImagination_Y = True
        yf += 1
    return Nodes, Bonds, PCs

def fracToAbsolute(*args):
    if len(args) == 5:
        return fracToAbsolute2D(*args)
    else:
        return fracToAbsolute3D(*args)
    
def getPoints(*args):
    if len(args) == 6:
        return getPoints2D(*args)
    else:
        return getPoints3D(*args)
    
def nodeDiary(node, nodes, bonds):
    incoming, outcoming = NBOSet(), NBOSet()
    for bond in bonds:
        if bond.node1 == node.num:
            outcoming.append(bond)
        if bond.node2 == node.num:
            incoming.append(bond)
    print(node.num, ':', node.x, node.y)
    NodeBonds = copy(incoming)
    for bond in outcoming:
        newBond = copy(bond)
        if bond in NodeBonds:
            newBond.num = len(NodeBonds.data) + 1
            newBond.shiftX, newBond.shiftY, newBond.shiftZ = -newBond.shiftX, -newBond.shiftY, -newBond.shiftZ  
        else:
            if len(NodeBonds.data) < bond.num or NodeBonds[bond.num]:
                newBond.num = len(NodeBonds.data) + 1
        NodeBonds.append(newBond)
    bondVectors = []
    i = 1
    for bond in NodeBonds:
        print('{:3}'.format("№" + str(i)), sep = '', end = ' ')
        i += 1
        if bond.node1 != node.num:
            nodeEnd = nodes[bond.node1]
            print(bond.node1, end = ' ')
        elif bond.node2 != node.num:
            nodeEnd = nodes[bond.node2]
            print(bond.node2, end = ' ')
        elif bond.node1 == bond.node2:
            nodeEnd = nodes[bond.node1]
            print(bond.node1, end = ' ')
        #print(node, nodeEnd)
        if nodeEnd.num < node.num:
            dx, dy, dz = nodeEnd.x + abs(bond.shiftX) - node.x, nodeEnd.y + abs(bond.shiftY) - node.y, nodeEnd.z + abs(bond.shiftZ) - node.z #Bug is here
        else:
            dx, dy, dz = nodeEnd.x + bond.shiftX - node.x, nodeEnd.y + bond.shiftY - node.y, nodeEnd.z + bond.shiftZ - node.z #Bug is here
        #print(dx, dy, dz)
        #if (dx, dy, dz) == (0, 0, 0):
            #print(node)
            #print(nodeEnd)
            #print(bond)
        bondVector = Vector(dx, dy, dz) 
        bondVectors.append(bondVector)
        print('{:12}|{:<05.3}'.format(str((bond.shiftX, bond.shiftY, bond.shiftZ)), bondVector.length(), end = '|'))
        print(' '.join('{:5}'.format(round(degrees(getAngle(bondVector, other)), 1)) for other in bondVectors if other != bondVector))
    # print(' ' * 26, end = '')
    for i in range(1, len([i for i in NodeBonds.data if i is not None])):
        print('{:>5}'.format('№' + str(i)), end = ' ')
    print()

def getCoveringLattice(primitiveCell):
    '''
    getCoveringLattice(primitiveCell) -> nodes, bonds
    Generates covering lattice for lattice in primitiveCell.
    '''
    nodes, bonds = igorToNBO(primitiveCell)
    newNodes = NBOSet()
    for bond in bonds:
        num = bond.num
        node1 = nodes[bond.node1]
        node2 = nodes[bond.node2]
        x1, y1, x2, y2 = node1.x, node1.y, node2.x, node2.y
        x, y = (x1 + x2 + bond.shiftX) / 2, (y1 + y2 + bond.shiftY) / 2
        newNodes.append(Node(num=num, x=x, y=y))
    newBonds = NBOSet()
    for node in nodes:
        incomingBonds = NBOSet()
        outcomingBonds = NBOSet()
        for bond in node.bonds:
            if bond.node1 == node.num:
                outcomingBonds.append(bond)
            if bond.node2 == node.num:
                incomingBonds.append(bond)
        for bond1 in incomingBonds:
            for bond2 in incomingBonds:
                newBond = Bond(num=len(newBonds.data) + 1, node1=bond1.num, node2=bond2.num, shiftX=bond1.shiftX - bond2.shiftX, shiftY=bond1.shiftY - bond2.shiftY)
                if newBond.node1 == newBond.node2 and newBond.shiftX == newBond.shiftY == 0:
                    continue
                if newBond not in newBonds:
                    newBonds.append(newBond)
                if newBond not in newNodes[bond1.num].bonds:
                    newNodes[bond1.num].bonds.append(newBond)
                if newBond not in newNodes[bond2.num].bonds:
                    newNodes[bond2.num].bonds.append(newBond)
        for bond1 in incomingBonds:
            for bond2 in outcomingBonds:
                newBond = Bond(num=len(newBonds.data) + 1, node1=bond1.num, node2=bond2.num, shiftX=bond1.shiftX, shiftY=bond1.shiftY)
                if newBond.node1 == newBond.node2 and newBond.shiftX == newBond.shiftY == 0:
                    continue
                if newBond not in newBonds:
                    newBonds.append(newBond)
                if newBond not in newNodes[bond1.num].bonds:
                    newNodes[bond1.num].bonds.append(newBond)
                if newBond not in newNodes[bond2.num].bonds:
                    newNodes[bond2.num].bonds.append(newBond)
        for bond1 in outcomingBonds:
            for bond2 in outcomingBonds:
                newBond = Bond(num=len(newBonds.data) + 1, node1=bond1.num, node2=bond2.num, shiftX=0, shiftY=0)
                if newBond.node1 == newBond.node2:
                    continue
                if newBond not in newBonds:
                    newBonds.append(newBond)
                if newBond not in newNodes[bond1.num].bonds:
                    newNodes[bond1.num].bonds.append(newBond)
                if newBond not in newNodes[bond2.num].bonds:
                    newNodes[bond2.num].bonds.append(newBond)
    return newNodes, newBonds