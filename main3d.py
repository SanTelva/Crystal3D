import pygame, sys
from pygame.locals import *
from copy import copy
from draw2.oldio import *
from draw2.graphics import *
from draw2.evaluations import *
from draw2.maths import *
from math import degrees

def whetherExit(Events):
    mainLoop = True
    global rotateMatrix, angleA, angleB, angleG, PC_Permission, readyNodes, readyBonds
    for event in Events:
        if event.type == QUIT:
            mainLoop = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                mainLoop = False
                print('exit')    
            elif event.key == K_p:
                PC_Permission = not PC_Permission
            elif event.key == K_HOME:
                rotateMatrix = Matrix()                    
            elif event.key == K_UP:
                rotateMatrix = rotateEvaluation('x', -angleF, rotateMatrix)
            elif event.key == K_DOWN:
                rotateMatrix = rotateEvaluation('x', angleF, rotateMatrix)            
            elif event.key == K_RIGHT:
                rotateMatrix = rotateEvaluation('y', -angleF, rotateMatrix)
            elif event.key == K_LEFT:
                rotateMatrix = rotateEvaluation('y', angleF, rotateMatrix)            
            elif event.key == K_PAGEUP:
                rotateMatrix = rotateEvaluation('z', -angleF, rotateMatrix)
            elif event.key == K_PAGEDOWN:
                rotateMatrix = rotateEvaluation('z', angleF, rotateMatrix)            
            elif event.key == K_d:
                for node in readyNodes:
                    nodeDiary(node, readyNodes, readyBonds)
    return mainLoop

# Graphical parameters ---- 
window_title = "Lattice"
window_bgcolor = (255, 255, 255)
lines_color = (0, 0, 0)
PC_color = (255, 150, 150)
PC_Permission = True

field_width = 1024 # in px
field_height = 768

angleF = 0.03

rotateMatrix = Matrix()

if len(sys.argv) < 2:
    print('Usage:')
    print(sys.argv[0], 'filename')
    raise ValueError
filename = sys.argv[1] # name of input file with ".txt"
angleA, angleB, angleG, a, b, c, PrimitiveCell = myInput(filename) # See draw2_input.py

#exit(0)
#----------------MAIN_LOOP--------------
# PyGame initialization
pygame.init()
screen = pygame.display.set_mode((field_width, field_height), 0, 32)
pygame.display.set_caption(window_title)
mainLoop = True
rotateMatrix = Matrix()

while mainLoop:
    # CONDITIONS OF 
    #print(pygame.event.get())
    mainLoop = whetherExit(pygame.event.get())
    
    #----------------------CREATING FRAME--------------------------------------
    screen.fill(window_bgcolor)
    
    #print("preEval")
    Nodes, Bonds, PCs, readyNodes, readyBonds = getPoints(angleA, angleB, angleG, a, b, c, PrimitiveCell, field_width, field_height)
    
    #print("postEval")
    # drawEverything()
    drawEverything(Nodes, Bonds, PCs, screen, lines_color, PC_color, angleA, angleB, angleG, a, b, c, rotateMatrix, PC_Permission)
    #pygame.draw.circle(screen, PC_color, (0, 0), 10)
    #print("Nodes:", "\n".join(map(str, Nodes)))
    #print("Bonds:", "\n".join(map(str, Bonds)))
    #print("PCs:", "\n".join(map(str, PCs)))
    # Finalize frame

    pygame.display.update()

    
pygame.quit()    
