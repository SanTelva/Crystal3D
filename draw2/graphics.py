import pygame, sys
from math import sqrt, exp
from pygame.locals import *
from draw2.evaluations import *


def reduce(x, y, z, matrix):
    '''
    turns vector _XYZ by the angle in matrix
    x, y, z - absolute coordinates of vector
    matrix - matrix object with angle rotating
    If you want turn the vector, you should multiplicate it onto rotating matrix. Types of matrixes are in draw2_maths
    rotateVector = Vector(x, y, z) - VectorCC, where vectorCC is vector from screen left head angle to your center of coordinates
    '''
    rotateVector = Vector(x, y, z) - Vector(512, 384, 0)
    return tuple(round(x) + 500 for x in matrix * rotateVector)

def brightness(z, color):
    return tuple(round(255 - (255 - i) * exp(-abs(z)/250)) for i in color)

def drawBonds3D(Bonds, screen, lines_color, angleA, angleB, angleG, a, b, c, rotateMatrix):
    for bond in Bonds:
        x0, y0, z0 = fracToAbsolute(bond[0], bond[1], bond[2], angleA, angleB, angleG, a, b, c)
        x1, y1, z1 = fracToAbsolute(bond[3], bond[4], bond[5], angleA, angleB, angleG, a, b, c)
        pygame.draw.line(screen, brightness(max(z0, z1), lines_color), reduce(x0, y0, z0, rotateMatrix)[:-1], reduce(x1, y1, z1, rotateMatrix)[:-1])

def drawNodes3D(Nodes, screen, lines_color, angleA, angleB, angleG, a, b, c, rotateMatrix):
    for node in Nodes:
        x, y, z = fracToAbsolute(node[0], node[1], node[2], angleA, angleB, angleG, a, b, c)
        pygame.draw.circle(screen, brightness(z, lines_color), reduce(x, y, z, rotateMatrix)[:-1], 5)
   
def drawPCs3D(PCs, screen, PC_color, angleA, angleB, angleG, a, b, c, rotateMatrix):
    for point in PCs:
        for line in point:
            x0, y0, z0 = fracToAbsolute(line[0], line[1], line[2], angleA, angleB, angleG, a, b, c)
            x1, y1, z1 = fracToAbsolute(line[3], line[4], line[5], angleA, angleB, angleG, a, b, c)
            pygame.draw.line(screen, brightness(min(z0, z1), PC_color), reduce(x0, y0, z0, rotateMatrix)[:-1], reduce(x1, y1, z1, rotateMatrix)[:-1])

def drawEverything3D(Nodes, Bonds, PCs, screen, lines_color, PC_color, angleA, angleB, angleG, a, b, c, rotateMatrix, PC_Permission):
    if PC_Permission:
        drawPCs(PCs, screen, PC_color, angleA, angleB, angleG, a, b, c, rotateMatrix)
    drawNodes(Nodes, screen, lines_color, angleA, angleB, angleG, a, b, c, rotateMatrix)
    drawBonds(Bonds, screen, lines_color, angleA, angleB, angleG, a, b, c, rotateMatrix)   
 
def drawBonds2D(Bonds, screen, lines_color, angle, a, b):
    for bond in Bonds:
        x0, y0 = fracToAbsolute(bond[0], bond[1], angle, a, b)
        x1, y1 = fracToAbsolute(bond[2], bond[3], angle, a, b)
        pygame.draw.line(screen, lines_color, (x0, y0), (x1, y1)) # Add

def drawNodes2D(Nodes, screen, lines_color, angle, a, b):
    for node in Nodes:
        x, y = fracToAbsolute(node[0], node[1], angle, a, b)
        pygame.draw.circle(screen, lines_color, (x,y), 10)
   
def drawPCs2D(PCs, screen, PC_color, angle, a, b):
    for point in PCs:
        for line in point:
            x0, y0 = fracToAbsolute(line[0], line[1], angle, a, b)
            x1, y1 = fracToAbsolute(line[2], line[3], angle, a, b)
            pygame.draw.line(screen, PC_color, (x0, y0), (x1, y1))

def drawEverything2D(Nodes, Bonds, PCs, screen, lines_color, PC_color, angle, a, b):
    drawBonds(Bonds, screen, lines_color, angle, a, b)
    drawNodes(Nodes, screen, lines_color, angle, a, b)
    drawPCs(PCs, screen, PC_color, angle, a, b)
    
def drawBonds(*args):
    if len(args) == 6:
        drawBonds2D(*args)
    else:
        drawBonds3D(*args)
        
def drawNodes(*args):
    if len(args) == 6:
        drawNodes2D(*args)
    else:
        drawNodes3D(*args)
        
def drawPCs(*args):
    if len(args) == 6:
        drawPCs2D(*args)
    else:
        drawPCs3D(*args)

def drawEverything(*args):
    if len(args) == 9:
        drawEverything2D(*args)
    else:
        drawEverything3D(*args)