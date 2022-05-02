import pygame, random, sys
from time import sleep
pygame.init()
pygame.font.init()

screenX = 500
screenY = 500
cellSize = 10


speed = 1

white = (255, 255, 255)
field = (0, 155, 0)  # green 0
wall = (0, 0, 0)  # black 1
head = (7, 127, 166)  # blue 2
body = (87, 0, 0)  # brown 3
food = (164, 0, 0)  # red 4


pygame.display.set_caption('Snake AI')
screen = pygame.display.set_mode([screenX, screenY])

cells = [
    [0 for _ in range(int(screenX/cellSize))]
    for _ in range(int(screenY/cellSize))
]


def drawCell(x, y, color = (0,0,0)):
    if screenX > x * cellSize >= 0 and screenY > y * cellSize >= 0:
        pygame.draw.rect(screen, color, (x * cellSize, y * cellSize, cellSize, cellSize), 0)


# def clear():
#     global cells
#     cells = [
#         [0 for _ in range(int(screenX / cellSize))]
#         for _ in range(int(screenY / cellSize))
#     ]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #place wall
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if i == 0 or i == len(cells) - 1 or j == 0 or j == len(cells) - 1 :
                cells[i][j] = 1


    #place food
    cells[5][6] = 4

    #place snake

    cells[25][15] = 2
    cells[25][16] = 3
    cells[25][17] = 3
    cells[25][18] = 3
    cells[25][19] = 3
    cells[25][20] = 3

    #draw cells
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
    sleep(speed)

pygame.quit()