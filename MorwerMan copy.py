# MowerMan 

import random, pygame, sys
from pygame.locals import *
import pygame.mixer

FPS = 7
WINDOWWIDTH = 600
WINDOWHEIGHT = 440
CELLSIZE = 40
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (0,     255, 0)
BLACK     = (  150,   75,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 155,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR =   (  0, 65,   0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


HEAD = 0 

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('MowerMan')
    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    mowerCoords = [{'x': startx,     'y': starty}]
    direction = RIGHT
    score = 0
    cutTwiceCoords = [{'x': -1, 'y':0 }]
    tractSound = pygame.mixer.Sound("tractGo.wav")
    tractSound.play()
    obstacles = [{'x': 4,     'y': 4},
                  {'x': 5, 'y': 4},
                  {'x': 6, 'y': 4},
                 {'x': 11,'y': 10},
                 {'x': 11,'y': 9},
                 {'x': 11,'y': 8},
                 {'x': 11,'y': 7}]

    finish = (WINDOWWIDTH/40) * (WINDOWHEIGHT/40) - len(obstacles)


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                    
        # check if mower hit the edge
        if mowerCoords[HEAD]['x'] == -1 or mowerCoords[HEAD]['x'] == CELLWIDTH or mowerCoords[HEAD]['y'] == -1 or mowerCoords[HEAD]['y'] == CELLHEIGHT:
            tractSound.stop()
            return # game over
        for cutGrass in mowerCoords[1:]:
            if cutGrass['x'] == mowerCoords[HEAD]['x'] and cutGrass['y'] == mowerCoords[HEAD]['y']:
                newCut = {'x': cutGrass['x'], 'y': cutGrass['y']}
                score = score - 2
                finish = finish + 1
                for grass in cutTwiceCoords:
                    if grass['x'] == mowerCoords[HEAD]['x'] and grass['y'] == mowerCoords[HEAD]['y']:
                        tractSound.stop()
                        return # game over
                cutTwiceCoords.insert(0, newCut)
        for obstacle in obstacles:
            if mowerCoords[HEAD]['x'] == obstacle['x'] and mowerCoords[HEAD]['y']== obstacle['y']:
                tractSound.stop()
                return
      
        score = score + 1
        finish = finish - 1;
        
        if finish == 0:
            showWinScreen()
            return

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': mowerCoords[HEAD]['x'], 'y': mowerCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': mowerCoords[HEAD]['x'], 'y': mowerCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': mowerCoords[HEAD]['x'] - 1, 'y': mowerCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': mowerCoords[HEAD]['x'] + 1, 'y': mowerCoords[HEAD]['y']}

        
        mowerCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrass(mowerCoords)
        drawGrass2(cutTwiceCoords)
        drawMower(newHead)
        drawObstacle(obstacles)
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 90)
    directionFont = pygame.font.Font('freesansbold.ttf', 20)
    titleSurf1 = titleFont.render('MOWERMAN!', True, WHITE, GREEN)
    firstLine = directionFont.render('Cut all the grass in he field', True, WHITE)
    secondLine = directionFont.render('Avoid The brown fences ', True, WHITE)
    thirdLine = directionFont.render('Be careful not to cut the grass to low or you will fail', True, WHITE)

    firstRect = firstLine.get_rect()
    secondRect = secondLine.get_rect()
    thirdRect = thirdLine.get_rect()
 
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedRect1 = titleSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, 100)
        DISPLAYSURF.blit(titleSurf1, rotatedRect1)

        firstRect = firstLine.get_rect()
        secondRect = secondLine.get_rect()
        thirdRect = thirdLine.get_rect()
        firstRect.midtop = (WINDOWWIDTH / 2, 200)
        secondRect.midtop = (WINDOWWIDTH / 2, secondRect.height + 200 + 15)
        thirdRect.midtop = (WINDOWWIDTH / 2, thirdRect.height + 200 + 45)



        DISPLAYSURF.blit(firstLine, firstRect)
        DISPLAYSURF.blit(secondLine, secondRect)
        DISPLAYSURF.blit(thirdLine, thirdRect)

        


        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return


def showWinScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('WINNER', True, RED)
    overSurf = gameOverFont.render('**********', True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2,WINDOWHEIGHT/2)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, RED)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawGrass(grassCoords):
    for coord in grassCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawMower(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrass2(grassCoords):
    for coord in grassCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)

def drawObstacle(coords):
    for coord in coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, BLACK, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BLACK, wormInnerSegmentRect)
    

if __name__ == '__main__':
    main()
