import pygame
from pygame.math import Vector2
from config import CELL_SIZE, CELL_NUMBER, COLORS

class Snake:
    def __init__(self):
        self.reset()

    def draw(self, screen):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            
            color = COLORS["head"] if index == 0 else COLORS["body"]
            pygame.draw.rect(screen, color, block_rect)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def grow(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def check_collision(self):
        head = self.body[0]
        if not (0 <= head.x < CELL_NUMBER and 0 <= head.y < CELL_NUMBER):
            return True
        for block in self.body[1:]:
            if head == block:
                return True
        return False

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)