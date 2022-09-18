import pygame

HEIGHT, WIDTH = 800, 800
ROWS, COLS = 8, 8
# how big is one square on checkerboard
SQUARE_SIZE = WIDTH//COLS

# RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load(
    'checkers/assets/crown.png'), (45, 25))
