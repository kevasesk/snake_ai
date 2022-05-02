import pygame, random, sys
from time import sleep
pygame.init()
pygame.font.init()

screenX = 500
screenY = 500
cellSize = 10


speed = 0.2

black = (0, 0, 0)
white = (255, 255, 255)
red = (164, 0, 0)

field = (0, 155, 0)  # green 0
wall = black  # black 1
head = (7, 127, 166)  # blue 2
body = (87, 0, 0)  # brown 3
food = red  # red 4

running = True
gameOnline = 1
score = 3

cells = [
    [0 for _ in range(int(screenX/cellSize))]
    for _ in range(int(screenY/cellSize))
]

moveDirection = 1
snakeHead = {
    'x': 25,
    'y': 15
}
snakeBody = [
    {
        'x': 25,
        'y': 16
    },
    {
        'x': 25,
        'y': 17
    },
    {
        'x': 25,
        'y': 18
    },
]

pygame.display.set_caption('Snake AI')
screen = pygame.display.set_mode([screenX + 200, screenY])
my_font = pygame.font.Font(pygame.font.get_default_font(), 32)



def drawCell(x, y, color = (0,0,0)):
    if screenX > x * cellSize >= 0 and screenY > y * cellSize >= 0:
        pygame.draw.rect(screen, color, (x * cellSize, y * cellSize, cellSize, cellSize), 0)

def clear():
    global cells
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            cells[i][j] = 0
def placeWalls():
    global cells
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if i == 0 or i == len(cells) - 1 or j == 0 or j == len(cells) - 1:
                cells[i][j] = 1
def placeFood():
    global cells
    cells[random.randint(1, int(screenX/cellSize) - 2)][random.randint(1, int(screenX/cellSize) - 2)] = 4

clear()
placeWalls()
placeFood()
while running:
    # render the text
    pygame.draw.rect(screen, black, (screenX, cellSize, 150, 50), 0)
    text_surface = my_font.render('Score: ' + str(score), True, white)
    screen.blit(text_surface, dest=(screenX, cellSize))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
        cells[snakeBody[-1]['x']][snakeBody[-1]['y']] = 0  # place field on old tail location
        snakeBody[-1]['x'] = headBeforeMove['x']  # place tail on old location of head
        snakeBody[-1]['y'] = headBeforeMove['y']  # place tail on old location of head

        snakeBody.insert(0, snakeBody[-1]) # place new body
        del snakeBody[-1]
        for snakePart in snakeBody:
            cells[snakePart['x']][snakePart['y']] = 3


        if cellBeforeMove == 1 or cellBeforeMove == 3:
            print('game over')
            gameOnline = 0
        if cellBeforeMove == 4:
            score += 1
            placeFood()
            snakeBody.append({
                'x': newTail['x'],
                'y': newTail['y']
            })

    print(score)
    if gameOnline:
        # draw cells
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if cells[i][j] == 0:
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
        pygame.draw.rect(screen, field, (int(screenX/2), int(screenY/2), 150, 50), 0)
        text_surface = my_font.render('Game Over!', True, red)
        screen.blit(text_surface, dest=(int(screenX/2) - 150 / 2 , int(screenY/2) - 50/2))
        pygame.display.flip()
    sleep(speed)

pygame.quit()