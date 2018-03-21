import json
from draw2.nbolib import *
from math import degrees, radians

def nboOutput(*args):
    if len(args) == 7:
        return nboOutput3D(*args)
    else:
        return nboOutput2D(*args)

def nboOutput3D(filename, angle, a, b, c, nodes, bonds):
    angleA, angleB, angleG = angle
    with open(filename, 'w') as outputFile:
        readyDict = dict()
        readyDict['geometry'] = {\
            'angleA': round(degrees(angleA)),\
                'angleB': round(degrees(angleB)),\
                    'angleG': round(degrees(angleG)),\
                        'sideA': a,\
                            'sideB': b,\
                                'sideC': c\
                                    }
        readyDict['topology'] = dict()
        readyDict['topology']['nodes'] = []
        for node in nodes:
            readyNode = {\
                'num': node.num,\
                    'x': node.x,\
                        'y': node.y,\
                            'z': node.z
                            }
            readyDict['topology']['nodes'].append(readyNode)
        readyDict['topology']['bonds'] = []
        for bond in bonds:
            readyBond = {\
                'num': bond.num,\
                    'node1': bond.node1,\
                        'node2': bond.node2,\
                            'shiftX': bond.shiftX,\
                                'shiftY': bond.shiftY,\
                                    'shiftZ': bond.shiftZ\
                                    }
            readyDict['topology']['bonds'].append(readyBond)
        readyString = json.dumps(readyDict, sort_keys=True, indent=4)
        print(readyString, file=outputFile)

def nboOutput2D(filename, angle, a, b, nodes, bonds):
    with open(filename, 'w') as outputFile:
        readyDict = dict()
        readyDict['geometry'] = {\
            'angle': round(degrees(angle)),\
                'sideA': a,\
                    'sideB': b\
                        }
        readyDict['topology'] = dict()
        readyDict['topology']['nodes'] = []
        for node in nodes:
            readyNode = {\
                'num': node.num,\
                    'x': node.x,\
                        'y': node.y\
                        }
            readyDict['topology']['nodes'].append(readyNode)
        readyDict['topology']['bonds'] = []
        for bond in bonds:
            readyBond = {\
                'num': bond.num,\
                    'node1': bond.node1,\
                        'node2': bond.node2,\
                            'shiftX': bond.shiftX,\
                                }
            readyDict['topology']['bonds'].append(readyBond)
        readyString = json.dumps(readyDict, sort_keys=True, indent=4)
        print(readyString, file=outputFile)
                    
def loadTopology(rawNodes, rawBonds):
    readyNodes = NBOSet()
    readyBonds = NBOSet()
    for rawNode in rawNodes:
        readyNode = Node(**rawNode)
        readyNodes.append(readyNode)
    for rawBond in rawBonds:
        readyBond = Bond(**rawBond)
        if readyBond not in readyNodes[readyBond.node1].bonds:
            readyNodes[readyBond.node1].bonds.append(readyBond)
        if readyBond not in readyNodes[readyBond.node2].bonds:
            readyNodes[readyBond.node2].bonds.append(readyBond)
        readyBonds.append(readyBond)
    return readyNodes, readyBonds
        
def load2D(rawDict):
    angle = radians(rawDict['geometry']['angle'])
    a = rawDict['geometry']['sideA']
    b = rawDict['geometry']['sideB']
    return angle, a, b

def load3D(rawDict):
    angleA = radians(rawDict['geometry']['angleA'])
    angleB = radians(rawDict['geometry']['angleB'])
    angleG = radians(rawDict['geometry']['angleG'])
    a = rawDict['geometry']['sideA']
    b = rawDict['geometry']['sideB']
    c = rawDict['geometry']['sideC']
    return angleA, angleB, angleG, a, b, c

def nboInput(filename):
    # Returns angle, a, b, nodes, bonds
    with open(filename, 'r') as inputFile:
        rawDict = json.loads(''.join(inputFile.readlines()))
        rawNodes = rawDict['topology']['nodes']
        rawBonds = rawDict['topology']['bonds']
        topology = loadTopology(rawNodes, rawBonds)
        if 'sideC' in rawDict['geometry']: # If file is 3d
            geometry = load3D(rawDict)
        else:
            geometry = load2D(rawDict)
    return geometry + topology

__all__ = ['nboOutput', 'nboOutput2D', 'nboOutput3D', 'nboInput']