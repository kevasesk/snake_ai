import pygame
import random
from pygame.math import Vector2
from config import CELL_SIZE, CELL_NUMBER, COLORS

class Food:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.randomize_position([])

    def draw(self, screen):
        x_pos = int(self.position.x * CELL_SIZE)
        y_pos = int(self.position.y * CELL_SIZE)
        food_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLORS["food"], food_rect)

    def randomize_position(self, snake_body):
        self.position = Vector2(random.randint(0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))
        while self.position in snake_body:
            self.position = Vector2(random.randint(0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))