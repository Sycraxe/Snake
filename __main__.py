from __future__ import annotations
from random import randint
import pygame

#Classes
class Controls:
    def __init__(self, up: int, down: int, left: int, right: int):
        if type(up) != int or type(down) != int or type(left) != int or type(right) != int:
            raise TypeError
        self.up, self.down, self.left, self.right = up, down, left, right

class Color:
    def __init__(self, r: int, g: int, b: int):
        if type(r) != int or type(g) != int or type(b) != int:
            raise TypeError
        self.r, self.g, self.b = r, g, b
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

class Ring:
    def __init__(self, x: int, y: int, next: Ring | None = None):
        if type(x) != int or type(y) != int:
            raise TypeError
        if type(next) != Ring and next is not None:
            raise TypeError
        self.x, self.y = x, y
        self.next = next
    
    def update(self, x: int, y: int):
        if type(x) != int or type(y) != int:
            raise TypeError
        self.x, self.y = x, y
    
    def draw(self, screen: pygame.surface.Surface, ratio: int, color: Color):
        if type(screen) != pygame.surface.Surface:
            raise TypeError
        if type(ratio) != int:
            raise TypeError
        if type(color) != Color:
            raise TypeError
        pygame.draw.rect(screen, color.to_tuple(), (self.x * ratio, self.y * ratio, ratio, ratio))


class Snake:
    def __init__(self, x: int, y: int, color: Color, controls: Controls, rings: int = 1):
        if type(x) != int or type(y) != int:
            raise TypeError
        if type(color) != Color:
            raise TypeError
        if type(controls) != Controls:
            raise TypeError
        if type(rings) != int:
            raise TypeError
        if rings < 1:
            raise ValueError
        self.dx, self.dy = 0, 0
        self.rings = rings
        self.ring = Ring(x, y)
        for _ in range(rings - 1):
            self.append()
        self.color = color
        self.controls = controls

    def update(self, width: int, height: int, events: list[pygame.event.Event], fruits: list[Fruit]):
        ring = self.ring
        x, y = ring.x, ring.y
        x_, y_ = 0, 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls.up:
                    if not (self.dx == 0 and self.dy == 1):
                        self.dx = 0
                        self.dy = -1
                if event.key == self.controls.down:
                    if not (self.dx == 0 and self.dy == -1):
                        self.dx = 0
                        self.dy = 1
                if event.key == self.controls.left:
                    if not (self.dx == 1 and self.dy == 0):
                        self.dx = -1
                        self.dy = 0
                if event.key == self.controls.right:
                    if not (self.dx == -1 and self.dy == 0):
                        self.dx = 1
                        self.dy = 0
        
        x += self.dx
        y += self.dy

        if x < 0 or x >= width or y < 0 or y >= height:
            self.reset(width, height)

        else:
            for fruit in fruits:
                if (fruit.x, fruit.y) == (x, y):
                    fruit.shuffle(width, height)
                    self.append()
            
            while ring != None:
                x_, y_ = ring.x, ring.y
                ring.update(x, y)
                ring = ring.next
                x, y = x_, y_
    
    def draw(self, screen: pygame.surface.Surface, ratio: int):
        ring = self.ring
        while ring != None:
            ring.draw(screen, ratio, self.color)
            ring = ring.next
    
    def append(self):
        ring = self.ring
        x, y = ring.x, ring.y
        while ring.next != None:
            ring = ring.next
            x, y = ring.x, ring.y
        ring.next = Ring(x, y)
    
    def reset(self, width: int, height: int):
        self.ring = Ring(randint(0, width - 1), randint(0, height - 1))
        for _ in range(self.rings - 1):
            self.append()
        self.dx, self.dy = 0, 0

class Fruit:
    def __init__(self, x: int = 0, y: int = 0):
        self.x, self.y = x, y
    
    def draw(self, screen: pygame.surface.Surface, ratio: int):
        pygame.draw.rect(screen, (0xff, 0x00, 0x00), (self.x * ratio, self.y * ratio, ratio, ratio))

    def shuffle(self, width: int, height: int):
        self.x, self.y = randint(0, width - 1), randint(0, height - 1)


#Game setup
width, height = 19, 19
ratio = 30

screen = pygame.display.set_mode((height * ratio, width * ratio), pygame.NOFRAME)
clock = pygame.time.Clock()

snakes = [Snake(9, 9, Color(0xFF, 0x00, 0xFF), Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT), 3)]
fruits = [Fruit(0, 0)]

run = True

#Main loop
while run:

    events = pygame.event.get()
    for snake in snakes:
        snake.update(width, height, events, fruits)

    screen.fill((0, 0, 0))

    for i in range(width):
        for j in range(height):
            pygame.draw.rect(screen, ((0x58, 0x81, 0x57) if (i + j) % 2 == 0 else (0x3a, 0x5a, 0x40)), (i * ratio, j * ratio, ratio, ratio))

    for snake in snakes:
        snake.draw(screen, ratio)

    for fruit in fruits:
        fruit.draw(screen, ratio)

    pygame.display.flip()

    clock.tick(10)

pygame.quit()