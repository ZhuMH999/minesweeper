import pygame

pygame.font.init()

WIDTH, HEIGHT = (800, 600)
SQUARE_SIZE = 50
ADJ_SQUARES = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]

COLORS = {0: (100, 100, 100),
          1: (0, 0, 255),
          2: (0, 255, 0),
          3: (255, 0, 0),
          4: (0, 0, 127),
          5: (255, 0, 255),
          6: (14, 124, 97),
          7: (255, 0, 255),
          8: (100, 100, 100),
          '*': (255, 255, 255)}

FONT = pygame.font.Font('minesweeper/mine-sweeper.ttf', 15)
SQUARE = pygame.transform.scale(pygame.image.load('minesweeper/square.png'), (SQUARE_SIZE, SQUARE_SIZE))