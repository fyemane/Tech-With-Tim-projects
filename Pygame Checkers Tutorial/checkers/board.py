# board class to represent checkers board
# handle piece movement, deleting pieces, drawing on screen
import pygame
# relative import within module
from checkers.constants import BLACK, COLS, RED, ROWS, SQUARE_SIZE, WHITE
from checkers.piece import Piece


class Board:
    def __init__(self):
        # internal representation of board
        # 2D list of two different pieces
        self.board = []
        # number of pieces of each side
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        # automatically create board when created
        self.create_board()

    # draw board
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            # draw square red for every other col
            # alternate starting btwn col 1 and 2
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE,
                                            SQUARE_SIZE, SQUARE_SIZE))

    # input row, col and outputs piece
    def get_piece(self, row, col):
        return self.board[row][col]

    # delete piece and move it
    def move(self, piece, row, col):
        # swap positions
        # piece in source pos swaps with piece in destination pos
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # check if we hit last row to become king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    # create board with pieces
    def create_board(self):
        for row in range(ROWS):
            # internal list for each row
            self.board.append([])
            for col in range(COLS):
                # if current col mod 2 equals row + 1, then draw piece
                # (row + 1) alternates between even and odd cols
                if col % 2 == ((row + 1) % 2):
                    # draw for first 3 rows
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    # draw after row 5
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        # blank separator
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        # draw pieces and squares
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                # don't draw piece for empty space
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        # replace pieces with empty
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0: 
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None
    
    def get_valid_moves(self, piece):
        # dictionary of keys 
        # move as destination key (row, col) : any pieces jumped
        # e.g., (4, 5) : [(3, 4)]
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # check whether to move up/down based on color or king
        if piece.color == RED or piece.king:
            # update moves with another dictionary 
            # row - 1 is moving up
            # max is far up to look
            ## row - 1 means to row 0
            ## row - 3 don't look further than 2 pieces away than currently am
            # -1 means move up when decrementing for loop
            # l eft is starting col and what to subtact when moving upwards
            # merges dictionary with moves dictionary
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            # moving 
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves


    # step is for moving up/down when traversing through rows for diagonal
    # skipped - if pieces skipped, then only move squares to skip another
    # left/right - starting col when going left/right
    # recursive, returns dictionary
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        # last piece to skip to move where to go
        last = []
        # what row to start/stop and the step
        for r in range(start, stop, step):
            # if looking outside board
            if left < 0:
                break
            current = self.board[r][left]
            # if current thing looking at is 0, found empty square
            if current == 0:
                # if skipped piece and can't skip again
                if skipped and not last:
                    break
                elif skipped:
                    # double jumping
                    moves[(r, left)] = last + skipped
                else:
                    # add as possible move
                    moves[(r, left)] = last
                # empty square last had value in it
                if last:
                    # had something skipped, preparing to double jump
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # call recursively
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            # if current has our color
            elif current.color == color:
                break
            # if current has opposing color
            else:
                last = [current]
    
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        # last piece to skip to move where to go
        last = []
        # what row to start/stop and the step
        for r in range(start, stop, step):
            # if looking outside board
            if right >= COLS:
                break
            current = self.board[r][right]
            # if current thing looking at is 0, found empty square
            if current == 0:
                # if skipped piece and can't skip again
                if skipped and not last:
                    break
                elif skipped:
                    # double jumping
                    moves[(r, right)] = last + skipped
                else:
                    # add as possible move
                    moves[(r, right)] = last
                # empty square last had value in it
                if last:
                    # had something skipped, preparing to double jump
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # call recursively
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            # if current has our color
            elif current.color == color:
                break
            # if current has opposing color
            else:
                last = [current]
    
            right += 1

        return moves
