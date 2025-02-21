"""
A simple Snake game implemented using Pygame.

This script defines a basic Snake game where the player controls a snake
that moves around the screen to eat apples. The game ends if the snake
collides with itself or the screen boundaries.
"""

from random import randrange
import sys
from time import sleep
import pygame
from pygame.event import Event


class Snake:
    """
    Represents the snake in the game.

    Attributes:
        head (pygame.Rect): The head of the snake.
        direction (str): The current direction of movement.
        color (str): The color of the snake.
        size (int): The size of each snake segment.
        game (Game): The game instance the snake belongs to.
        parts (list[pygame.Rect]): List of all segments forming the snake.
        min_move_delay (int): Minimum delay between movements.
        move_delay_step (int): Step by which movement delay decreases.
        move_delay (int): Current movement delay.
        last_move_time (int): Last recorded time of movement.
    """

    def __init__(self, game: "Game", position: pygame.Vector2 = None) -> None:
        """
        Initializes the snake at a random position.

        Args:
            game (Game): The game instance the snake belongs to.
            position (pygame.Vector2, optional): Starting position of the snake. Defaults to None.
        """
        self.game = game
        self.size = self.game.object_size
        if position is None:
            position = self.game.get_random_position()
        self.head = pygame.Rect(position, (self.size, self.size))
        self.direction = "RIGHT"
        self.color = "GREEN"
        self.parts = [self.head]
        self.min_move_delay = 50
        self.move_delay_step = 5
        self.move_delay = 200
        self.last_move_time = pygame.time.get_ticks()

    def move(self) -> None:
        """
        Moves the snake in current direction.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time <= self.move_delay:
            return

        for i in range(len(self.parts) - 1, 0, -1):
            self.parts[i].topleft = self.parts[i - 1].topleft

        if self.direction == "UP":
            self.head.y -= self.size
        if self.direction == "DOWN":
            self.head.y += self.size
        if self.direction == "LEFT":
            self.head.x -= self.size
        if self.direction == "RIGHT":
            self.head.x += self.size
        self.last_move_time = current_time
        self.check_collision()

    def check_collision(self) -> None:
        """
        Checks for collision with apple, itself, or screen boundaries.
        """
        if (
            any(self.head.colliderect(part) for part in self.parts[1:])
            or self.head.x not in range(int(self.game.screen_size.x))
            or self.head.y not in range(int(self.game.screen_size.y))
        ):
            self.game.running = False
            print(any(self.head.colliderect(part) for part in self.parts[1:]))

        if self.head.colliderect(self.game.apple.rect):
            self.grow()
            self.increase_speed()
            self.game.apple = Apple(self.game)

    def grow(self) -> None:
        """
        Adds a new segment to the snake
        """
        last_part = self.parts[-1]
        new_part = pygame.Rect(last_part.topleft, (self.size, self.size))
        if self.direction == "UP":
            new_part.y += self.size
        elif self.direction == "DOWN":
            new_part.y -= self.size
        elif self.direction == "LEFT":
            new_part.x += self.size
        elif self.direction == "RIGHT":
            new_part.x -= self.size
        self.parts.append(new_part)

    def increase_speed(self):
        """
        Increases speed of snake by reducing movement delay.
        """
        self.move_delay = max(
            self.min_move_delay, self.move_delay - self.move_delay_step
        )


class Apple:
    """
    Represents an apple in the game that the snake can eat.

    Attributes:
        color (str): The color of the apple
        rect (pygame.Rect): The rectangular area occupied by the apple.
    """

    def __init__(self, game: "Game", old_position: pygame.Vector2 = None):
        """
        Initializes an apple at a random position, ensuring it does not spawn on the snake.

        Args:
            game (Game): The game instance the apple belongs to.
            old_position (pygame.Vector2, optional): The previous apple position. Defaults to None.
        """
        new_position = game.get_random_position()
        while new_position == old_position or any(
            new_position == part.topleft for part in game.snake.parts[1:]
        ):
            new_position = game.get_random_position()
        self.color = "RED"
        self.rect = pygame.Rect(new_position, (game.object_size, game.object_size))


class Game:
    """
    Manages the main game logic and state.

    Attributes:
        screen_size (pygame.Vector2): The dimensions of the game window.
        object_size (int): The size of each object in the game.
        screen (Surface): The Pygame window surface.
        clock (pygame.time.Clock): Controls the game speed.
        snake (Snake): The snake object.
        apple (Apple): The apple object.
        running (bool): Indicates if the game is currently running.
    """

    def __init__(self) -> None:
        """
        Initializes game. Sets up Pygame, creates the game objects and defines game settings.
        """
        pygame.init()
        self.display_flags = pygame.NOFRAME
        self.screen_size = pygame.Vector2(800, 600)
        self.object_size = 20
        self.screen = pygame.display.set_mode(self.screen_size, self.display_flags)
        self.clock = pygame.time.Clock()
        self.snake = Snake(game=self)
        self.apple = Apple(game=self)
        self.running = True

    def get_random_position(self) -> pygame.Vector2:
        """
        Generates a random position withing the screen grid.

        Returns:
            pygame.Vector2: A valid position for game objects.
        """
        return pygame.Vector2(
            randrange(int(self.screen_size.x // self.object_size)) * self.object_size,
            randrange(int(self.screen_size.y // self.object_size)) * self.object_size,
        )

    def handle_input(self, events: list[Event]) -> None:
        """
        Process player input to control the snake.

        Args:
            events (list[Event]): List of Pygame events.
        """
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
            if event.type == pygame.QUIT:
                self.running = False
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
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def get_score(self):
        score = len(self.snake.parts)
        score_text = pygame.font.SysFont("cooperblack", 24).render(
            str(score), True, "WHITE"
        )
        return score_text

    def draw(self) -> None:
        """
        Draws the game objects on the screen.
        """
        self.screen.fill("black")
        self.screen.blit(self.get_score(), (10, 10))
        for part in self.snake.parts:
            pygame.draw.rect(self.screen, self.snake.color, part)
        pygame.draw.rect(self.screen, self.apple.color, self.apple.rect)
        pygame.display.flip()

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        while self.running:
            self.handle_input(events=pygame.event.get())
            self.snake.move()
            self.snake.check_collision()
            self.draw()
            self.clock.tick(60)
        self.game_over()

    def game_over(self):
        """
        Handles Game Over screen
        """
        self.screen = pygame.display.set_mode(self.screen_size)
        game_over_text = pygame.font.SysFont("cooperblack", 64).render(
            "GAME OVER", True, "WHITE"
        )
        game_over_text_rect = game_over_text.get_rect(
            center=(self.screen_size.x / 2, self.screen_size.y / 2)
        )
        self.screen.blit(game_over_text, game_over_text_rect)
        pygame.display.flip()
        while not self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.screen = pygame.display.set_mode(
                        self.screen_size, flags=self.display_flags
                    )
                    self.running = True
                    self.snake = Snake(self)
                    self.apple = Apple(self)
        self.run()


if __name__ == "__main__":
    game_inst = Game()
    game_inst.run()
