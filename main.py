import pygame, random, sys
from time import sleep

import brain

pygame.init()
pygame.font.init()


cellSize = 10
screenX = 20 * cellSize
screenY = 20 * cellSize

speed = 0.01

black = (0, 0, 0)
white = (255, 255, 255)
red = (164, 0, 0)

field = (0, 155, 0)  # green 5
wall = black  # black 1
head = (7, 127, 166)  # blue 2
body = (87, 0, 0)  # brown 3
food = red  # red 4

running = True
gameOnline = 1
score = 0

cells = [
    [5 for _ in range(int(screenX/cellSize))]
    for _ in range(int(screenY/cellSize))
]

moveDirection = 1
snakeHead = {
    'x': int(screenX/cellSize/2),
    'y': int(screenY/cellSize/2),
}
snakeBody = [
    {
        'x': int(screenX/cellSize/2),
        'y': int(screenY/cellSize/2) + 1
    },
]

pygame.display.set_caption('Snake AI')
screen = pygame.display.set_mode([screenX + 100, screenY])
my_font = pygame.font.Font(pygame.font.get_default_font(), 15)



def drawCell(x, y, color = (0,0,0)):
    if screenX > x * cellSize >= 0 and screenY > y * cellSize >= 0:
        pygame.draw.rect(screen, color, (x * cellSize, y * cellSize, cellSize, cellSize), 0)

def clear():
    global cells
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            cells[i][j] = 5
def placeWalls():
    global cells
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if i == 0 or i == len(cells) - 1 or j == 0 or j == len(cells) - 1:
                cells[i][j] = 1
def placeFood():
    global cells
    cells[random.randint(1, int(screenX/cellSize) - 2)][random.randint(1, int(screenX/cellSize) - 2)] = 4

def getDirection(newDir, oldDir):
    if newDir == 1 and oldDir == 3:
        return oldDir
    if newDir == 2 and oldDir == 4:
        return oldDir
    if newDir == 3 and oldDir == 1:
        return oldDir
    if newDir == 4 and oldDir == 2:
        return oldDir
    return newDir


def newGame():
    global score, cells, moveDirection, snakeHead, snakeBody, gameOnline
    cells = [
        [5 for _ in range(int(screenX / cellSize))]
        for _ in range(int(screenY / cellSize))
    ]
    placeWalls()
    placeFood()
    gameOnline = 1
    score = 0

    moveDirection = 1
    snakeHead = {
        'x': int(screenX / cellSize / 2),
        'y': int(screenY / cellSize / 2),
    }
    snakeBody = [
        {
            'x': int(screenX / cellSize / 2),
            'y': int(screenY / cellSize / 2) + 1
        },
    ]


clear()
placeWalls()
placeFood()

new_game_surface = my_font.render('New Game', True, white)
screen.blit(new_game_surface, dest=(screenX, cellSize+20))
currentBrain = None
while running:
    # render the text
    pygame.draw.rect(screen, black, (screenX, cellSize, 100, 20), 0)
    text_surface = my_font.render('Score: ' + str(score), True, white)
    screen.blit(text_surface, dest=(screenX, cellSize))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            print(mouse)
            if 230 <= mouse[0] <= 260 and 20 <= mouse[1] <= 50:
                print('new game')
                newGame()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if moveDirection != 3:
                    moveDirection = 1
            if event.key == pygame.K_RIGHT:
                if moveDirection != 4:
                    moveDirection = 2
            if event.key == pygame.K_DOWN:
                if moveDirection != 1:
                    moveDirection = 3
            if event.key == pygame.K_LEFT:
                if moveDirection != 2:
                    moveDirection = 4

    if gameOnline == 1:
        headBeforeMove = {
            'x': snakeHead['x'],
            'y': snakeHead['y']
        }

        # brain start

        if not currentBrain:
            currentBrain = brain.networkInit(cells, 300, 4)
        else:
            currentBrain = brain.networkBuild(cells, currentBrain['w1'], currentBrain['w2'])

        moveDirection = getDirection(currentBrain['direction'], moveDirection)



        if moveDirection == 1:  # up
            snakeHead = {
                'x': snakeHead['x'],
                'y': snakeHead['y'] - 1
            }
        if moveDirection == 2:  # right
            snakeHead = {
                'x': snakeHead['x'] + 1,
                'y': snakeHead['y']
            }
        if moveDirection == 3:  # down
            snakeHead = {
                'x': snakeHead['x'],
                'y': snakeHead['y'] + 1
            }
        if moveDirection == 4:  # left
            snakeHead = {
                'x': snakeHead['x'] - 1,
                'y': snakeHead['y']
            }

        cellBeforeMove = cells[snakeHead['x']][snakeHead['y']]
        cells[snakeHead['x']][snakeHead['y']] = 2  # place head on new location

        newTail = {
            'x': snakeBody[-1]['x'],
            'y': snakeBody[-1]['y']
        }
        cells[snakeBody[-1]['x']][snakeBody[-1]['y']] = 5  # place field on old tail location
        snakeBody[-1]['x'] = headBeforeMove['x']  # place tail on old location of head
        snakeBody[-1]['y'] = headBeforeMove['y']  # place tail on old location of head

        snakeBody.insert(0, snakeBody[-1]) # place new body
        del snakeBody[-1]
        for snakePart in snakeBody:
            cells[snakePart['x']][snakePart['y']] = 3


        if cellBeforeMove == 1 or cellBeforeMove == 3:
            gameOnline = 0
        if cellBeforeMove == 4:
            score += 1
            placeFood()
            snakeBody.append({
                'x': newTail['x'],
                'y': newTail['y']
            })

    if gameOnline:
        # draw cells
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if cells[i][j] == 5:
                    drawCell(i, j, field)
                if cells[i][j] == 1:
                    drawCell(i, j, wall)
                if cells[i][j] == 2:
                    drawCell(i, j, head)
                if cells[i][j] == 3:
                    drawCell(i, j, body)
                if cells[i][j] == 4:
                    drawCell(i, j, food)
        pygame.display.flip()
    else:
        if score >= 1:
            if len(brain.individuals) < brain.population:
                brain.individuals.append({
                    'w1': currentBrain['w1'],
                    'w2': currentBrain['w2']
                })
            if len(brain.individuals) == brain.population:
                brain.nextGeneration()
                pass
        currentBrain = brain.networkInit(cells, 300, 4)
        print(len(brain.individuals))
        newGame()
        # pygame.draw.rect(screen, field, (int(screenX/2), int(screenY/2), 150, 50), 0)
        # text_surface = my_font.render('Game Over!', True, red)
        # screen.blit(text_surface, dest=(int(screenX/2) - 50 / 2 , int(screenY/2) - 25/2))
        # pygame.display.flip()
    sleep(speed)

pygame.quit()