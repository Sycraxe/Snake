import pygame

W, H = 19, 19
RATIO = 30

DARK_GREEN = (0x3a, 0x5a, 0x40)
LIGHT_GREEN = (0x58, 0x81, 0x57)

screen = pygame.display.set_mode((H * RATIO, W * RATIO), pygame.NOFRAME)
clock = pygame.time.Clock()
run = True
x, y = W//4, H//2

def draw_checkerboard():
    for i in range(W):
        for j in range(H):
            pygame.draw.rect(screen, (LIGHT_GREEN if (i + j) % 2 == 0 else DARK_GREEN), (i * RATIO, j * RATIO, RATIO, RATIO))

def draw_snake(x, y):
    pygame.draw.rect(screen, (0xff, 0xff, 0xff), (x * RATIO, y * RATIO, RATIO, RATIO))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y -= 1
            if event.key == pygame.K_DOWN:
                y += 1
            if event.key == pygame.K_LEFT:
                x -= 1
            if event.key == pygame.K_RIGHT:
                x += 1

    clock.tick(60)

    screen.fill((0, 0, 0))
    draw_checkerboard()
    draw_snake(x, y)
    pygame.display.flip()

pygame.quit()