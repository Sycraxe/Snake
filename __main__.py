from __future__ import annotations
from typing import List
from random import randint
import pygame

width, height = 19, 19
RATIO = 30

screen = pygame.display.set_mode((height * RATIO, width * RATIO), pygame.NOFRAME)
clock = pygame.time.Clock()
run = True

class Ring:
    def __init__(self, x: int, y: int, next: Ring | None = None):
        self.next = next
        self.x, self.y = x, y
    
    def update(self, x: int, y: int):
        self.x, self.y = x, y
    
    def draw(self):
        pygame.draw.rect(screen, (0xff, 0xff, 0xff), (self.x * RATIO, self.y * RATIO, RATIO, RATIO))

class Snake:
    def __init__(self, x: int = 0, y: int = 0):
        if type(x) != int or type(y) != int:
            raise TypeError
        self.ring = Ring(x, y)
        self.dx, self.dy = 0, 0

    def update(self, width: int, height: int, events: List[pygame.event.Event], fruits: List[Fruit]):
        ring = self.ring
        x, y = ring.x, ring.y
        x_, y_ = 0, 0

        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.dx = 0
                    self.dy = -1
                if event.key == pygame.K_DOWN:
                    self.dx = 0
                    self.dy = 1
                if event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0
                if event.key == pygame.K_RIGHT:
                    self.dx = 1
                    self.dy = 0
        
        x += self.dx
        y += self.dy

        for fruit in fruits:
            if fruit.location() == (x, y):
                fruit.shuffle(width, height)
                self.append()

        while ring != None:
            x_, y_ = ring.x, ring.y
            ring.update(x, y)
            ring = ring.next
            x, y = x_, y_
    
    def draw(self):
        ring = self.ring
        while ring != None:
            ring.draw()
            ring = ring.next
    
    def append(self):
        ring = self.ring
        x, y = ring.x, ring.y
        while ring.next != None:
            ring = ring.next
            x, y = ring.x, ring.y
        ring.next = Ring(x - self.dx, y - self.dy)

class Fruit:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x, self.y = x, y
    
    def draw(self):
        pygame.draw.rect(screen, (0xff, 0x00, 0x00), (self.x * RATIO, self.y * RATIO, RATIO, RATIO))

    def shuffle(self, width: int, height: int):
        self.x, self.y = randint(0, width - 1), randint(0, height - 1)
    
    def location(self):
        return (self.x, self.y)

snake = Snake(width//4, height//2)
fruits = [Fruit(randint(0, width - 1), randint(0, height - 1)) for i in range(1)]

while run:

    snake.update(width, height, pygame.event.get(), fruits)
    clock.tick(10)

    screen.fill((0, 0, 0))

    #Checkerboard
    for i in range(width):
        for j in range(height):
            pygame.draw.rect(screen, ((0x58, 0x81, 0x57) if (i + j) % 2 == 0 else (0x3a, 0x5a, 0x40)), (i * RATIO, j * RATIO, RATIO, RATIO))

    snake.draw()
    for fruit in fruits:
        fruit.draw()

    pygame.display.flip()

pygame.quit()