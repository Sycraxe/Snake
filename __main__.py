from __future__ import annotations
import pygame

W, H = 19, 19
RATIO = 30

DARK_GREEN = (0x3a, 0x5a, 0x40)
LIGHT_GREEN = (0x58, 0x81, 0x57)

screen = pygame.display.set_mode((H * RATIO, W * RATIO), pygame.NOFRAME)
clock = pygame.time.Clock()
run = True

def draw_checkerboard():
    for i in range(W):
        for j in range(H):
            pygame.draw.rect(screen, (LIGHT_GREEN if (i + j) % 2 == 0 else DARK_GREEN), (i * RATIO, j * RATIO, RATIO, RATIO))

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

    def update(self, key: int = 0):
        ring = self.ring
        x, y = ring.x, ring.y
        x_, y_ = 0, 0

        if key == pygame.K_UP:
            y -= 1
        if key == pygame.K_DOWN:
            y += 1
        if key == pygame.K_LEFT:
            x -= 1
        if key == pygame.K_RIGHT:
            x += 1

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
        pass


snake = Snake(W//4, H//2)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:
            snake.update(event.key)
        else:
            snake.update()

    clock.tick(60)

    screen.fill((0, 0, 0))
    draw_checkerboard()
    snake.draw()
    pygame.display.flip()

pygame.quit()