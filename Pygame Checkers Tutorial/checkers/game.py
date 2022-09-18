# handling game mechanics
# turns, selecting and moving pieces, drawing
# want game operated to computers, not linked in directly to user events
# game exposes methods, independent of user input
import pygame
from checkers.board import Board
from checkers.constants import BLUE, RED, SQUARE_SIZE, WHITE


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    # update pygame display
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # private method, can't be called
    def _init(self):
        # if piece is selected
        self.selected = None
        self.board = Board()
        self.turn = RED
        # valid moves to play
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    # reset game
    def reset(self):
        self._init()

    # tell row and col selected
    # use game info to then do something
    def select(self, row, col):
        # if piece already selected, move piece to row and col
        if self.selected:
            # try to move it to destination
            result = self._move(row, col)
            # if invalid, then try to select different piece
            if not result:
                # reset selection and reselect row and col, recursive
                self.selected = None
                self.select(row, col)
        # don't accidentally run code after recursion
        # if selection is valid
        piece = self.board.get_piece(row, col)
        # if not selecting empty piece and during turn
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # if selected empty destination
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # move currently selected piece to row and col
            self.board.move(self.selected, row, col)
            # check if position moved to has piece skipped
            skipped = self.valid_moves[(row, col)]
            if skipped:
                # remove skipped piece
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    # draw squares for valid moves
    def draw_valid_moves(self, moves):
        for move in moves:
            # all moves are dictionary
            # loops through all key tuples in dictionary
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        # remove blue circle, blank list
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        