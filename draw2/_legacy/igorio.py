from math import *

def formatPC3D(inputFile):
    '''
    Returns list, containing nodes. Each node is list [num, x, y, z, [bonds]] where:
    "num" is number of node (numeration starts from 1)
    "x", "y", "z" are coords of node, relative to primitive cell.
    Each bond is list [shiftX, shiftY, shiftZ, num] where:
    "shiftX", "shiftY", "shiftZ" are shifts in primitive cells to other node.
    "num" is number of other node.
    '''
    # FORMATTING DATA
    # Primitive Cell nodes
    lines = [node.split("\t") for node in inputFile.readlines()]# Get list of lists of strings
    if lines[-1] == []:
        lines = lines[:-1]
    primitiveCell = []
    for i in range(len(lines)):
        node = lines[i]
        node = [float(x) for x in node[0:4]] + [list(map(int, x.split())) for x in node[4:]]
        node[0] = int(node[0])
        primitiveCell.append(node)
        
    return tuple(primitiveCell)

def formatPC2D(inputFile):
    '''
    Returns list, containing nodes. Each node is list [num, x, y, [bonds]] where:
    "num" is number of node (numeration starts from 1)
    "x" and "y" are coords of node, relative to primitive cell.
    Each bond is list [shiftX, shiftY, num] where:
    "shiftX" and "shiftY" are shifts in primitive cells to other node.
    "num" is number of other node.
    '''
    # FORMATTING DATA
    # Primitive Cell nodes
    lines = [node.split("\t") for node in inputFile.readlines()] # Get list of lists of strings
    primitiveCell = []
    for i in range(len(lines)):
        node = lines[i]
        # print("node:", node)
        node = [float(x) for x in node[0:3]] + [list(map(int, x.split())) for x in node[3:]]
        node[0] = int(node[0])
        primitiveCell.append(node)
        
    return tuple(primitiveCell)

#---------------------------------INPUT-----------------------------------------
def myInput3D(filename):
    with open(filename) as inputFile:
        temp = list(map(float, inputFile.readline().split()))
        angleA = radians(temp[0])
        angleB = radians(temp[1])
        angleG = radians(temp[2])
        a = temp[3]
        b = temp[4]
        c = temp[5]
        primitiveCell = formatPC3D(inputFile)    
        return angleA, angleB, angleG, a, b, c, primitiveCell

def myInput2D(filename):
    with open(filename) as inputFile:
    
        temp = list(map(float, inputFile.readline().split()))
        
        # Post-INPUT parameters
    
        # Primitive Cell form (parallelogram) 
        angle = radians(temp[0])
        a = temp[1]
        b = temp[2]
        # print("angle:", angle, "a:", a, "b:", b)
    
        primitiveCell = formatPC2D(inputFile)    
        # print("PC:", primitiveCell)
    
        return angle, a, b, primitiveCell

def myInput(filename):
    '''
    FileFormat - Igor3D
    A - angle xOz
    B - angle xOy
    G - angle y0z
    myInput(filename) -> first angle, second angle, diagonal angle a, b, c, primitiveCell
    Returns data from file.
    "angle" is angle between primitive cell side.
    "a", "b", "c" are lengths of primitive cell sides
    "primitiveCell" is list, containing nodes. Each node is list [num, x, y, [bonds]] where:
    "num" is number of node (numeration starts from 1)
    "x", "y", "z" are coords of node, relative to primitive cell.
    Each bond is list [shiftX, shiftY, shiftZ, num] where:
    "shiftX", "shiftY", "shiftZ" are shifts in primitive cells to other node.
    "num" is number of other node.
    '''
    # *Input format description*
    # Numerate nodes from "1", please!
    with open(filename) as inputFile:
        temp = list(map(float, inputFile.readline().split()))
        if len(temp) > 3:
            return myInput3D(filename)
        else:
            return myInput2D(filename)

def myOutput2D(filename, primitiveCell):
    with open(filename, 'w') as outputFile:
        print(round(degrees(primitiveCell[0])), primitiveCell[1], primitiveCell[2], file=outputFile)
        ################if type(primitiveCell[3]) == type(()): # Using myInput() like primitive cell. # PLEASE, DO NOT UNCOMMENT THIS TRASH AND DO NOT USE IT.
        rawData = primitiveCell[3]
        for node in rawData:
            print(node)
            print(node[0], node[1], node[2], sep="\t", end="\t", file=outputFile)
            rawBonds = node[3:]
            readyBonds = []
            for rawBond in rawBonds:
                readyBonds.append(' '.join(map(str, rawBond)))
            if len(readyBonds) != 0:
                print(readyBonds)
                print("\t".join(readyBonds), file=outputFile)
            else:
                print('0 0', node[0], file=outputFile)    

def myOutput3D(filename, primitiveCell):
    '''
    myOutput(filename, primitiveCell) -> None
    Outputs primitiveCell to file "filename".
    '''
    with open(filename, 'w') as outputFile:
        print(round(degrees(primitiveCell[0])), round(degrees(primitiveCell[1])), round(degrees(primitiveCell[2])),\
            primitiveCell[3], primitiveCell[4], primitiveCell[5], file=outputFile)
        rawData = primitiveCell[6]
        for node in rawData:
            print(node[0], node[1], node[2], node[3], sep="\t", end="\t", file=outputFile)
            rawBonds = node[4:]
            readyBonds = []
            for rawBond in rawBonds:
                readyBonds.append(' '.join(map(str, rawBond)))
            if len(readyBonds) != 0:
                print("\t".join(readyBonds), file=outputFile)
            else:
                print('0 0 0', node[0], file=outputFile)
            from math import radians
            
def myOutput(filename, primitiveCell):
    if type(primitiveCell[3]) == type(0.0) or type(primitiveCell[3]) == type(0):
        myOutput3D(filename, primitiveCell)
    else:
        myOutput2D(filename, primitiveCell) 
