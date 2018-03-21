import pygame, sys
from pygame.locals import *

from draw2.oldio import *
from draw2.graphics import *
from draw2.evaluations import *

def whetherExit(Events):
    mainLoop = True
    for event in Events:
        if event.type == QUIT:
            mainLoop = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                mainLoop = False
                print('exit')           
    return mainLoop

def toggleCovering(Events):
    result = False
    for event in Events:
        if event.type == KEYDOWN:
            if event.key == K_c:
                result = True
    return result

def toggleMain(Events):
    result = False
    for event in Events:
        if event.type == KEYDOWN:
            if event.key == K_d:
                result = True
    return result

#-------------------------PROGRAM PARAMETERS------------------------------------
#-------------------------(including INPUT)-------------------------------------

# Graphical parameters ---- 
window_title = "Lattice"
window_bgcolor = (255, 255, 255)
lines_color = (0, 0, 0)
PC_color = (255, 0, 0)
covering_color = (0, 56, 212)

field_width = 1000 # in px
field_height = 750

if len(sys.argv) < 2:
    print('Usage:')
    print(sys.argv[0], 'filename')
    raise ValueError
filename = sys.argv[1] # name of input file with ".txt"
angle, a, b, PrimitiveCell = myInput(filename) # See draw2_input.py

#exit(0)
#----------------MAIN_LOOP--------------
# PyGame initialization
pygame.init()
screen = pygame.display.set_mode((field_width, field_height), 0, 32)
pygame.display.set_caption(window_title)
mainLoop = True
drawCovering = False
drawMain = True

while mainLoop:
    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    # CONDITIONS OF EXIT
    Events = pygame.event.get()
    mainLoop = whetherExit(Events)
    drawCovering ^= toggleCovering(Events)
    drawMain ^= toggleMain(Events)
    #----------------------CREATING FRAME--------------------------------------
    screen.fill(window_bgcolor)
    
    _, _, PCs = getPoints(angle, a, b, PrimitiveCell, field_width, field_height)
    drawPCs(PCs, screen, PC_color, angle, a, b)
    
    if drawMain:
        Nodes, Bonds, PCs = getPoints(angle, a, b, PrimitiveCell, field_width, field_height)
        drawEverything(Nodes, Bonds, [], screen, lines_color, PC_color, angle, a, b)
        
    if drawCovering:
        coveringNBONodes, coveringNBOBonds = getCoveringLattice((angle, a, b, PrimitiveCell))
        coveringPC = nboToIGOR(coveringNBONodes, coveringNBONodes, angle, a, b)
        CoveringNodes, CoveringBonds, CoveringPCs = getPoints(coveringPC[0], coveringPC[1], coveringPC[2], coveringPC[3], field_width, field_height)
        drawEverything(CoveringNodes, CoveringBonds, [], screen, covering_color, PC_color, angle, a, b)
        
    #print("Nodes:", "\n".join(map(str, Nodes)))
    #print("Bonds:", "\n".join(map(str, Bonds)))
    #print("PCs:", "\n".join(map(str, PCs)))
    # Finalize frame
    pygame.display.update()
    # while True:
    #     pass
     
    
pygame.quit()    
 
