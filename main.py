import random
import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = (800, 600)
SQUARE_SIZE = 50
constants = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
FONT = pygame.font.SysFont('Arial', 15)


class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((0, 0, 0))
        for i in range(self.model.y):
            for j in range(self.model.x):
                pygame.draw.rect(self.win, (255, 255, 255), (SQUARE_SIZE*j, SQUARE_SIZE*i, SQUARE_SIZE, SQUARE_SIZE), width=1)
                if 's' in self.model.board[j][i]:
                    self.get_text_widget_and_center((255, 255, 255), SQUARE_SIZE * j + 25, SQUARE_SIZE * i + 25, FONT, self.model.board[j][i].split('s')[0])
                elif 'F' in self.model.board[i][j]:
                    self.get_text_widget_and_center((255, 255, 255), SQUARE_SIZE * j + 25, SQUARE_SIZE * i + 25, FONT, 'F')

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)


class Model:
    def __init__(self):
        self.x = 8
        self.y = 8
        self.board = [['0' for _ in range(self.x)] for _ in range(self.y)]
        self.setup_board()

    def dfs_check(self, cellx, celly, check_current_cell=False):
        if check_current_cell and 'F' not in self.board[celly][cellx]:
            self.board[celly][cellx] += 's'
        if '0' in self.board[celly][cellx] and 'F' not in self.board[celly][cellx]:
            for constant in constants:
                if -1 < cellx + constant[0] < self.x and -1 < celly + constant[1] < self.y:
                    if self.board[celly + constant[1]][cellx + constant[0]] != 'M' and 's' not in self.board[celly + constant[1]][cellx + constant[0]]:
                        self.board[celly + constant[1]][cellx + constant[0]] = self.board[celly + constant[1]][cellx + constant[0]].split('F')[0]
                        self.board[celly + constant[1]][cellx + constant[0]] += 's'
                        if '0' in self.board[celly + constant[1]][cellx + constant[0]]:
                            self.dfs_check(cellx + constant[0], celly + constant[1])

    def setup_board(self):
        for j in range(8):
            done = False
            while not done:
                temp_x, temp_y = random.randint(0, self.x - 1), random.randint(0, self.y - 1)
                if self.board[temp_y][temp_x] != 'M':
                    self.board[temp_y][temp_x] = 'M'
                    done = True
                    
        for a in range(self.y):
            for b in range(self.x):
                counter = 0
                for constant in constants:
                    if -1 < b + constant[0] < self.x and -1 < a + constant[1] < self.y:
                        if self.board[a + constant[1]][b + constant[0]] == 'M':
                            counter += 1
                if self.board[a][b] != 'M':
                    self.board[a][b] = str(counter)

    def check_where_mouse_clicked(self, x, y):
        if 0 < x < SQUARE_SIZE*self.x and 0 < y < SQUARE_SIZE*self.y:
            print(x//SQUARE_SIZE)
            self.dfs_check(y//SQUARE_SIZE, x//SQUARE_SIZE, True)

    def flag_piece(self, x, y):
        if 0 < x < SQUARE_SIZE * self.x and 0 < y < SQUARE_SIZE * self.y:
            if 's' not in self.board[y//SQUARE_SIZE][x//SQUARE_SIZE]:
                if 'F' in self.board[y//SQUARE_SIZE][x//SQUARE_SIZE]:
                    self.board[y // SQUARE_SIZE][x // SQUARE_SIZE] = self.board[y//SQUARE_SIZE][x//SQUARE_SIZE].split('F')[0]
                else:
                    self.board[y//SQUARE_SIZE][x//SQUARE_SIZE] += 'F'


class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Minesweeper')

        self.model = Model()
        self.view = View(self.model, self.win)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
