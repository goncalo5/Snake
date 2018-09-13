#!/usr/bin/env python
import random
import pygame
pygame.init()


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


# SETTINGS
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
MAROON = (128,  0,   0)

# Screen
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
FPS = 10

# Snake
SNAKE_INIT_POSX = 2
SNKAE_INIT_POSY = 1
SNAKE_INIT_SIZE = 3
SNAKE_THICKNESS = 20
# SNAKE_SPEED = 10
# Food
FOOD_WIDTH = 10
FOOD_HEIGHT = 10


class Food(object):
    def __init__(self, game):
        self.x = random.randint(0, DISPLAY_WIDTH)
        self.y = random.randint(0, DISPLAY_HEIGHT)

        self.obj = pygame.draw.rect(game.display, RED, (self.x, self.y, FOOD_WIDTH, FOOD_HEIGHT))

    def update(self, game):
        if self.obj.colliderect(game.snake.sections[0]):
            # print "colidio"
            self.x = random.randint(0, DISPLAY_WIDTH)
            self.y = random.randint(0, DISPLAY_HEIGHT)
            game.snake.size += 1

        self.obj = pygame.draw.rect(game.display, RED, (self.x, self.y, FOOD_WIDTH, FOOD_HEIGHT))


class Snake(object):
    def __init__(self, game):
        # self.speed = SNAKE_SPEED
        self.x = SNAKE_INIT_POSX
        self.y = SNKAE_INIT_POSY
        self.dx = 0  # self.speed
        self.dy = 1
        self.thickness = SNAKE_THICKNESS
        self.color = WHITE
        self.size = SNAKE_INIT_SIZE
        self.coords = [[self.x, self.y]]
        for section in range(self.size):
            if section == 0:
                continue
            print section
            x = self.x - section
            self.coords.append([x, self.y])
        print "self.coords", self.coords
        self.update_section(game)

    def update_coords(self):
        # print "\n\nupdate_coords", self.x, self.y, self.dx, self.dy
        old_coords = self.coords
        self.x += self.dx
        self.y += self.dy
        self.coords = [[self.x, self.y]]
        for section in range(self.size):
            if section == 0:
                continue
            x = old_coords[section - 1][0]
            y = old_coords[section - 1][1]
            self.coords.append([x, y])
            # print "self.coords", self.coords

    def update_section(self, game):
        # print "\nupdate_section", "self.coords", self.coords
        self.sections = []
        for section in self.coords:
            x = int(section[0] * self.thickness)
            y = int(section[1] * self.thickness)
            self.sections.append(pygame.draw.circle(game.display, self.color,
                                                    (x, y),
                                                    self.thickness / 2))

    def update(self, game):
        self.update_coords()
        self.update_section(game)
        if self.x * self.thickness > DISPLAY_WIDTH:
            self.x = 0
        if self.x * self.thickness < 0:
            self.x = DISPLAY_WIDTH / self.thickness
        if self.y * self.thickness > DISPLAY_HEIGHT:
            self.y = 0
        if self.y * self.thickness < 0:
            self.y = DISPLAY_HEIGHT / self.thickness

    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT]:
                if self.dx == 0:
                    self.dx = 1
                    self.dy = 0
            if event.key in [pygame.K_LEFT]:
                if self.dx == 0:
                    self.dx = -1
                    self.dy = 0
            if event.key in [pygame.K_UP]:
                if self.dy == 0:
                    self.dx = 0
                    self.dy = -1
                # self.deltas[0][0] = 0

            if event.key in [pygame.K_DOWN]:
                if self.dy == 0:
                    self.dx = 0
                    self.dy = 1


class Game(object):
    def __init__(self):
        self.cmd_key_down = False
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()

        self.snake = Snake(self)
        self.food = Food(self)
        # print type()

        self.loop()

    def loop(self):
        while True:
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                self.handle_common_keys(event)
                self.snake.handle_events(self, event)
            self.snake.update(self)
            self.food.update(self)
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_common_keys(self, event):
        if event.type == pygame.QUIT:
            self.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pygame.K_q:
                self.quit()

        if event.type == pygame.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def quit(self):
        pygame.quit()
        quit()


Game()
