import sys
sys.path += ['..']
from draw2.nbolib import *
from draw2.maths import *
from draw2.nboio import *
from math import sin, cos, sqrt

EPSILON = 0.5

def getDistance(angleA, angleB, angleG, a, b, c, x1, y1, z1, x2, y2, z2):
    def fracToAbsolute(xf, yf, zf, angleA, angleB, angleG, a, b, c):
        kx = cos(angleA)
        ky = (cos(angleG) - kx * cos(angleB)) / sin(angleB)
        vect_i = Vector(1, 0, 0)
        vect_j = Vector(cos(angleB), sin(angleB), 0)
        vect_k = Vector(kx, ky, sqrt(1 - kx ** 2 - ky ** 2))  
        return (round(coordinate) for coordinate in tuple(vect_i * xf * a + vect_j * yf * b + vect_k * zf * c))

    x1, y1, z1 = fracToAbsolute(x1, y1, z1, angleA, angleB, angleG, a, b, c)
    x2, y2, z2 = fracToAbsolute(x2, y2, z2, angleA, angleB, angleG, a, b, c)
    x = x2 - x1
    y = y2 - y1
    z = z2 - z1
    return sqrt(x ** 2 + y ** 2 + z ** 2)

def genBondsByNodes(angleA, angleB, angleG, a, b, c, nodes):
    # Returns bonds
    bonds = NBOSet()
    # Pregenerated list of all shifts by x, y and z.
    allShifts = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1), (-1, 0, -1), (-1, 0, 0), (-1, 0, 1), (-1, 1, -1), (-1, 1, 0), (-1, 1, 1), (0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 0, -1), (0, 0, 0), (0, 0, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1), (1, -1, -1), (1, -1, 0), (1, -1, 1), (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 1, -1), (1, 1, 0), (1, 1, 1)]
    for node1 in nodes:
        minDistance = 1337.0
        for shifts in allShifts:
            shiftX, shiftY, shiftZ = shifts
            for node2 in nodes:
                if node2.num == node1.num and shifts == (0, 0, 0):
                    continue
                x = node2.x + shiftX
                y = node2.y + shiftY
                z = node2.z + shiftZ
                dist = getDistance(angleA, angleB, angleG, a, b, c, x, y, z, node1.x, node1.y, node1.z)
                if dist < minDistance:
                    minDistance = dist
        # print('Min distance:', minDistance)
        for shifts in allShifts:
            shiftX, shiftY, shiftZ = shifts
            for node2 in nodes:
                x = node2.x + shiftX
                y = node2.y + shiftY
                z = node2.z + shiftZ
                dist = getDistance(angleA, angleB, angleG, a, b, c, x, y, z, node1.x, node1.y, node1.z)
                # print('Curr distance:', dist)
                # print('Curr shift:', shiftX, shiftY, shiftZ)
                if abs(dist - minDistance) < EPSILON:
                    newBond = Bond(num=len(bonds.data) + 1, node1=node1.num, node2=node2.num, shiftX=shiftX, shiftY=shiftY, shiftZ=shiftZ)
                    reversedBond = Bond(num=-1, node1=node2.num, node2=node1.num, shiftX=-shiftX, shiftY=-shiftY, shiftZ=-shiftZ)
                    if newBond not in bonds and reversedBond not in bonds:
                        bonds.append(newBond)
    return bonds

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:', sys.argv[0], 'input.nbo3d ouptut.nbo3d')
        __import__('_sitebuiltins').Quitter('','')(1) # exit(1)
    angleA, angleB, angleG, a, b, c, nodes, _ = nboInput(sys.argv[1])
    bonds = genBondsByNodes(angleA, angleB, angleG, a, b, c, nodes)
    nodes, bonds = syncNBO(nodes, bonds)
    nboOutput(sys.argv[2], (angleA, angleB, angleG), a, b, c, nodes, bonds)