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
    
    def draw(self, screen: pygame.surface.Surface, ratio: int, border: int, color: Color):
        if type(screen) != pygame.surface.Surface:
            raise TypeError
        if type(ratio) != int:
            raise TypeError
        if type(border) != int:
            raise TypeError
        if type(color) != Color:
            raise TypeError
        pygame.draw.rect(screen, color.to_tuple(), ((self.x + border) * ratio, (self.y + border) * ratio, ratio, ratio))


class Snake:
    def __init__(self, x: int, y: int, color: Color, controls: Controls, rings: int):
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
        self.score = 0

    def update(self, width: int, height: int, events: list[pygame.event.Event], fruits: list[Fruit], taken: list[tuple[int, int]]):
        if type(width) != int or type(height) != int:
            raise TypeError
        if type(events) != list:
            raise TypeError
        for event in events:
            if type(event) != pygame.event.Event:
                raise TypeError
        if type(fruits) != list:
            raise TypeError
        for fruit in fruits:
            if type(fruit) != Fruit:
                raise TypeError
        if type(taken) != list:
            raise TypeError
        for loc in taken:
            if type(loc) != tuple or len(loc) != 2 or type(loc[0]) != int or type(loc[1]) != int:
                raise TypeError
        
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
            return

        for loc in taken:
            if (x, y) == loc and (self.dx, self.dy) != (0, 0):
                self.reset(width, height)
                return

        for fruit in fruits:
            if (fruit.x, fruit.y) == (x, y):
                fruit.shuffle(width, height)
                self.append()
                self.score += 1
        
        while ring != None:
            x_, y_ = ring.x, ring.y
            ring.update(x, y)
            ring = ring.next
            x, y = x_, y_
    
    def draw(self, screen: pygame.surface.Surface, ratio: int, border: int):
        if type(screen) != pygame.surface.Surface:
            raise TypeError
        if type(ratio) != int:
            raise TypeError
        if type(border) != int:
            raise TypeError
        ring = self.ring
        while ring != None:
            ring.draw(screen, ratio, border, self.color)
            ring = ring.next
    
    def append(self):
        ring = self.ring
        x, y = ring.x, ring.y
        while ring.next != None:
            ring = ring.next
            x, y = ring.x, ring.y
        ring.next = Ring(x, y)
    
    def reset(self, width: int, height: int):
        if type(width) != int or type(height) != int:
            raise TypeError
        self.ring = Ring(randint(0, width - 1), randint(0, height - 1))
        for _ in range(self.rings - 1):
            self.append()
        self.dx, self.dy = 0, 0
        self.score = 0
    
    def locations(self) -> list[tuple[int, int]]:
        locations = []
        ring = self.ring
        while ring != None:
            locations.append((ring.x, ring.y))
            ring = ring.next
        return locations

class Fruit:
    def __init__(self, x: int = 0, y: int = 0):
        self.x, self.y = x, y
    
    def draw(self, screen: pygame.surface.Surface, ratio: int, border: int):
        if type(screen) != pygame.surface.Surface:
            raise TypeError
        if type(ratio) != int:
            raise TypeError
        if type(border) != int:
            raise TypeError
        pygame.draw.rect(screen, (0xB3, 0x36, 0x36), ((self.x + border) * ratio, (self.y + border) * ratio, ratio, ratio))

    def shuffle(self, width: int, height: int):
        if type(width) != int or type(height) != int:
            raise TypeError
        self.x, self.y = randint(0, width - 1), randint(0, height - 1)


#Game setup
width, height = 19, 19
border = 2
ratio = 30

pygame.init()

screen = pygame.display.set_mode(((height + 2*border) * ratio, (width + 2*border) * ratio), pygame.NOFRAME)
clock = pygame.time.Clock()

colors = [Color(0xB3, 0x59, 0xB3), Color(0x59, 0xAB, 0xB3), Color(0x59, 0xB3, 0x92), Color(0xAA, 0xB3, 0x59)]
controls = [Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT), 
            Controls(pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d), 
            Controls(pygame.K_t, pygame.K_g, pygame.K_f, pygame.K_h), 
            Controls(pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l)]

snakes = [Snake(randint(0, width - 1), randint(0, height - 1), colors[i], controls[i], 3) for i in range(2)]
fruits = [Fruit(randint(0, width - 1), randint(0, height - 1))]

font = pygame.font.Font("8bitoperator.ttf", 32)

plus = font.render("+", False, (0xDF, 0xDF, 0xDF))
minus = font.render("-", False, (0xDF, 0xDF, 0xDF))
cross = font.render("X", False, (0xB3, 0x36, 0x36))
credits = font.render("@sycraxe", False, (0x3a, 0x5a, 0x40))

plus_rect = plus.get_rect().move((width - 0.7) * ratio, (border - 1) * ratio)
minus_rect = minus.get_rect().move((width + 0.3) * ratio, (border - 1) * ratio)
cross_rect = cross.get_rect().move(((border + width + 0.7)) * ratio, 0.5 * ratio)
credits_rect = credits.get_rect().move(border * ratio, (border + height) * ratio)

run = True

#Main loop
while run:

    taken = []
    for snake in snakes:
        taken += snake.locations()

    events = pygame.event.get()
    for snake in snakes:
        snake.update(width, height, events, fruits, taken)
    
    pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if plus_rect.collidepoint(pos) and len(snakes) < 4:
                snakes.append(Snake(randint(0, width - 1), randint(0, height - 1), colors[len(snakes)], controls[len(snakes)], 3))
            if minus_rect.collidepoint(pos) and len(snakes) > 1:
                snakes.pop()
            if cross_rect.collidepoint(pos):
                run = False

    screen.fill((0x49, 0x6E, 0x4C))

    for i in range(width):
        for j in range(height):
            pygame.draw.rect(screen, ((0x58, 0x81, 0x57) if (i + j) % 2 == 0 else (0x3a, 0x5a, 0x40)), ((i + border) * ratio, (j + border) * ratio, ratio, ratio))

    for i, snake in enumerate(snakes):
        snake.draw(screen, ratio, border)
        screen.blit(font.render("P" + str(i+1) + ": " + str(snake.score), False, snake.color.to_tuple()), ((border + (width // 4) * i) * ratio, (border - 1) * ratio))

    if len(snakes) > 1: screen.blit(minus, minus_rect)
    if len(snakes) < 4: screen.blit(plus, plus_rect)
    screen.blit(cross, cross_rect)
    screen.blit(credits, credits_rect)

    for fruit in fruits:
        fruit.draw(screen, ratio, border)

    pygame.display.flip()

    clock.tick(10)

pygame.quit()