import pygame
import sys
from config import *
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        
        pygame.time.set_timer(pygame.USEREVENT, GAME_SPEED)

    def run(self):
        while True:
            while self.running:
                self.handle_events()
                self.draw_elements()
                self.clock.tick(60)

            self.show_game_over()
            self.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and self.running:
                self.update()
            if event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)

    def handle_key_press(self, key):
        if key == pygame.K_UP and self.snake.direction.y != 1:
            self.snake.direction = pygame.math.Vector2(0, -1)
        elif key == pygame.K_DOWN and self.snake.direction.y != -1:
            self.snake.direction = pygame.math.Vector2(0, 1)
        elif key == pygame.K_LEFT and self.snake.direction.x != 1:
            self.snake.direction = pygame.math.Vector2(-1, 0)
        elif key == pygame.K_RIGHT and self.snake.direction.x != -1:
            self.snake.direction = pygame.math.Vector2(1, 0)

    def update(self):
        self.snake.move()
        self.check_food_collision()
        if self.snake.check_collision():
            self.running = False

    def check_food_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 1
            self.food.randomize_position(self.snake.body)

    def draw_elements(self):
        self.screen.fill(COLORS["field"])
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_score()
        pygame.display.update()

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, COLORS["white"])
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        if AUTO_RESTART_ON_DEATH:
            return
        self.screen.fill(COLORS["black"])
        game_over_text = self.font.render(f'Game Over! Final Score: {self.score}', True, COLORS["white"])
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        self.screen.blit(game_over_text, text_rect)

        play_again_text = self.font.render('Play Again', True, COLORS["white"])
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        pygame.draw.rect(self.screen, COLORS["head"], play_again_rect.inflate(20, 10))
        self.screen.blit(play_again_text, play_again_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        waiting = False

    def reset(self):
        self.snake.reset()
        self.food.randomize_position([])
        self.score = 0
        self.running = True

game = Game()
game.run()