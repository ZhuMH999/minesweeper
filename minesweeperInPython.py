import random
import pygame
import math
from minesweeper.constants import FONT, FONT2_1, FONT2_2, SQUARE, WIDTH, HEIGHT, SQUARE_SIZE, COLORS

constants = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]

pygame.init()
pygame.font.init()

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        x, y = pygame.mouse.get_pos()
        self.win.fill((200, 200, 200))

        if self.model.x is not None:
            for i in range(self.model.y):
                for j in range(self.model.x):
                    pygame.draw.rect(self.win, (150, 150, 150), (SQUARE_SIZE*j, SQUARE_SIZE*i, SQUARE_SIZE, SQUARE_SIZE), width=2)
    
                    if 's' not in self.model.board[i][j]:
                        self.win.blit(SQUARE, (SQUARE_SIZE*j, SQUARE_SIZE*i, SQUARE_SIZE, SQUARE_SIZE))

                    if (('s' in self.model.board[i][j] and self.model.end is None) or self.model.end is not None) and '*' in self.model.board[i][j]:
                        self.get_text_widget_and_center(COLORS[self.model.board[i][j].split('s')[0].split('F')[0]], SQUARE_SIZE * j + SQUARE_SIZE/2, SQUARE_SIZE * i + SQUARE_SIZE/2, FONT, self.model.board[i][j].split('s')[0].split('F')[0])
                    elif ('s' in self.model.board[i][j] and self.model.end is None) or self.model.end is not None:
                        self.get_text_widget_and_center(COLORS[int(self.model.board[i][j].split('s')[0].split('F')[0])], SQUARE_SIZE * j + SQUARE_SIZE/2, SQUARE_SIZE * i + SQUARE_SIZE/2, FONT, self.model.board[i][j].split('s')[0].split('F')[0])
                    elif 'F' in self.model.board[i][j]:
                        self.get_text_widget_and_center((255, 255, 255), SQUARE_SIZE * j + 25, SQUARE_SIZE * i + 25, FONT, 'F')

            if self.model.end is not None:
                pygame.draw.rect(self.win, (90, 90, 90), (250, 195, 300, 190), border_radius=4)
                pygame.draw.rect(self.win, (210, 210, 210), (255, 200, 290, 180), border_radius=4)
                self.get_text_widget_and_center((200, 0, 0), 400, 225, FONT2_1, 'Game Over!')

                pygame.draw.rect(self.win, (100, 100, 100), (265, 265, 130, 60), border_radius=20)
                if 265 < x < 395 and 270 < y < 330:
                    pygame.draw.rect(self.win, (170, 170, 170), (270, 270, 120, 50), border_radius=20)

                pygame.draw.rect(self.win, (100, 100, 100), (405, 265, 130, 60), border_radius=20)
                if 405 < x < 535 and 270 < y < 330:
                    pygame.draw.rect(self.win, (170, 170, 170), (410, 270, 120, 50), border_radius=20)

                pygame.draw.rect(self.win, (100, 100, 100), (345, 335, 110, 40), border_radius=20)
                if 345 < x < 455 and 335 < y < 375:
                    pygame.draw.rect(self.win, (170, 170, 170), (350, 340, 100, 30), border_radius=20)

                self.get_text_widget_and_center((238, 238, 210), 330, 295, FONT2_2, 'Play Again')
                self.get_text_widget_and_center((238, 238, 210), 470, 295, FONT2_2, 'Main Menu')
                self.get_text_widget_and_center((238, 238, 210), 400, 355, FONT2_2, 'Quit Game')

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)


class Model:
    def __init__(self):
        self.run = True
        self.x = 15
        self.y = 10
        self.mine_count = 30
        self.end = None
        self.board = [['0' for _ in range(self.x)] for _ in range(self.y)]
        self.clicked = False

    def dfs_check(self, cellx, celly, check_current_cell=False):
        if check_current_cell and 'F' not in self.board[celly][cellx]:
            self.board[celly][cellx] += 's'
        if '0' in self.board[celly][cellx] and 'F' not in self.board[celly][cellx]:
            for constant in constants:
                if -1 < cellx + constant[0] < self.x and -1 < celly + constant[1] < self.y:
                    if self.board[celly + constant[1]][cellx + constant[0]] != '*' and 's' not in self.board[celly + constant[1]][cellx + constant[0]]:
                        self.board[celly + constant[1]][cellx + constant[0]] = self.board[celly + constant[1]][cellx + constant[0]].split('F')[0]
                        self.board[celly + constant[1]][cellx + constant[0]] += 's'
                        if '0' in self.board[celly + constant[1]][cellx + constant[0]]:
                            self.dfs_check(cellx + constant[0], celly + constant[1])

    @staticmethod
    def check_for_adj(x, y, minex, miney):
        if x == minex and y == miney:
            return False
        for constant in constants:
            if y + constant[1] == miney and x + constant[0] == minex:
                return False
        return True

    def setup_board(self, x, y):
        for j in range(self.mine_count):
            done = False
            while not done:
                temp_x, temp_y = random.randint(0, self.x - 1), random.randint(0, self.y - 1)
                if self.board[temp_y][temp_x] != '*' and self.check_for_adj(x, y, temp_x, temp_y):
                    self.board[temp_y][temp_x] = '*'
                    done = True
                    
        for a in range(self.y):
            for b in range(self.x):
                counter = 0
                for constant in constants:
                    if -1 < b + constant[0] < self.x and -1 < a + constant[1] < self.y:
                        if self.board[a + constant[1]][b + constant[0]] == '*':
                            counter += 1
                if self.board[a][b] != '*':
                    self.board[a][b] = str(counter)

    def check_where_mouse_clicked(self, x, y):
        if 0 < x < SQUARE_SIZE*self.x and 0 < y < SQUARE_SIZE*self.y and self.end is None:
            if not self.clicked:
                self.setup_board(x//SQUARE_SIZE, y//SQUARE_SIZE)
                self.clicked = True
            self.dfs_check(x//SQUARE_SIZE, y//SQUARE_SIZE, True)
            self.check_for_end(x//SQUARE_SIZE, y//SQUARE_SIZE)

        elif self.end is not None:
            if 265 < x < 395 and 270 < y < 330:
                self.x = 15
                self.y = 10
                self.mine_count = 30
                self.end = None
                self.board = [['0' for _ in range(self.x)] for _ in range(self.y)]
                self.clicked = False

            if 405 < x < 535 and 270 < y < 330:
                self.x = None

            if 345 < x < 455 and 335 < y < 375:
                self.run = False

    def flag_piece(self, x, y):
        if 0 < x < SQUARE_SIZE * self.x and 0 < y < SQUARE_SIZE * self.y and self.end is None:
            if 's' not in self.board[y//SQUARE_SIZE][x//SQUARE_SIZE]:
                if 'F' in self.board[y//SQUARE_SIZE][x//SQUARE_SIZE]:
                    self.board[y // SQUARE_SIZE][x // SQUARE_SIZE] = self.board[y//SQUARE_SIZE][x//SQUARE_SIZE].split('F')[0]
                else:
                    self.board[y//SQUARE_SIZE][x//SQUARE_SIZE] += 'F'

    def check_for_end(self, x, y):
        if '*' in self.board[y][x] and 's' in self.board[y][x]:
            self.end = False
            print('game over')

        counter = 0
        for i in range(self.y):
            for j in range(self.x):
                if 's' in self.board[i][j] and '*' not in self.board[i][j]:
                    counter += 1

        if self.x * self.y - self.mine_count == counter:
            self.end = True
            print('win')

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Minesweeper')

        self.model = Model()
        self.view = View(self.model, self.win)

    def run(self):
        self.model.run = True

        while self.model.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        self.model.check_where_mouse_clicked(x, y)
                    elif event.button == 3:
                        self.model.flag_piece(x, y)

            self.view.draw()
            pygame.display.update()


if __name__ == '__main__':
    c = Controller()
    c.run()
