import pygame
from checkers.constants import CROWN, GREY, SQUARE_SIZE


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        # calculate position
        self.calc_pos()

    # calculate pos based on row and col
    def calc_pos(self):
        # center of circular piece in middle of square
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # piece becomes king
    def make_king(self):
        self.king = True

    # draw piece itself
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        # draw outline
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        # draw small circle with padding
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, 
            self.y - CROWN.get_height()/2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    # what is internal representation
    def __repr__(self):
        return str(self.color)
