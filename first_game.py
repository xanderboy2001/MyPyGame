import pygame
from pygame.locals import *
from random import randint
from typing import Tuple


class Snake:
    def __init__(
        self, color: str = "GREEN", init_direction: str = "RIGHT", size: int = 20
    ):
        self.head = pygame.Rect((20, 20), (size, size))
        self.direction = init_direction
        self.color = color
        self.size = size
        self.parts = []
        self.parts.append(self.head)


class Apple:
    def __init__(
        self, old_position: pygame.Vector2 = None, color: str = "RED", size: int = 20
    ):
        while True:
            x_pos = randint(0, pygame.display.get_surface().get_width() // size) * size
            y_pos = randint(0, pygame.display.get_surface().get_height() // size) * size
            new_position = pygame.Vector2(x_pos, y_pos)
            if new_position != old_position:
                break
        self.color = color
        self.rect = pygame.Rect(new_position, (size, size))


class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.NOFRAME
        self.screen = pygame.display.set_mode((800, 600), flags, vsync=1)
        self.clock = pygame.time.Clock()
        self.move_delay = 200
        self.last_move_time = pygame.time.get_ticks()
        self.snake = Snake()
        self.apple = Apple()
        self.counter = 0
        self.min_move_delay = 50
        self.move_delay_step = 50

    def handle_input(self, events):
        key_to_direction = {
            pygame.K_UP: "UP",
            pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_d: "RIGHT",
        }
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in key_to_direction:
                    new_direction = key_to_direction[event.key]
                    if (
                        (new_direction == "UP" and self.snake.direction != "DOWN")
                        or (new_direction == "DOWN" and self.snake.direction != "UP")
                        or (new_direction == "LEFT" and self.snake.direction != "RIGHT")
                        or (new_direction == "RIGHT" and self.snake.direction != "LEFT")
                    ):
                        self.snake.direction = new_direction
                elif event.key == pygame.K_z:
                    self.counter += 1
                    print(f"Z key pressed {self.counter} times!")
                    self.move_delay = max(
                        self.min_move_delay, self.move_delay - self.move_delay_step
                    )
                    print(f"Snake speed increased! Move delay: {self.move_delay}ms")

    def move_snake(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time <= self.move_delay:
            return

        if self.snake.direction == "UP":
            self.snake.head.y -= self.snake.size
        if self.snake.direction == "DOWN":
            self.snake.head.y += self.snake.size
        if self.snake.direction == "LEFT":
            self.snake.head.x -= self.snake.size
        if self.snake.direction == "RIGHT":
            self.snake.head.x += self.snake.size

        if self.snake.head.colliderect(self.apple.rect):
            print("Apple Eaten!")
            self.apple = Apple()
        self.last_move_time = current_time

    def draw(self):
        self.screen.fill("black")
        pygame.draw.rect(self.screen, self.snake.color, self.snake.head)
        pygame.draw.rect(self.screen, self.apple.color, self.apple.rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False
            self.handle_input(events)
            self.move_snake()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
