# copy board multiple times
# make 
# shallow copy = copy reference
# deep copy = copy reference and object
import pygame
from copy import deepcopy
 

RED = (255, 0, 0)
WHITE = (255, 255, 255)

# position = current position we are in (board object)
# depth = how far to extend tree (recursive call)
# max_player = boolean to either max/min value
# game = game object in main.py file
def minimax(position, depth, max_player, game):
    # determine depth, only evaluate position at end of tree (depth = 0)
    if depth == 0 or position.winner() != None:
        # if game won, then game over and stop evaluating
        # if depth is 0, get evaluation, and return position with evaluation
        return position.evaluate(), position
    # maximize score
    if max_player:
        # max eval seen so far
        # whenever checking new position at beginning, best seen is -inf
        maxEval = float('-inf')
        # store best move
        best_move = None
        # for every move to make
        for move in get_all_moves(position, WHITE, game):
            # evaluate move by recursively recall by going down depth
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            # if move is best seen so far
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
            
    else:
        minEval = float('inf')
        # store best move
        best_move = None
        for move in get_all_moves(position, RED, game):
            # evaluate move by recursively recall by going down depth
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = max(minEval, evaluation)
            # if move is best seen so far
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

# all possible moves from current board 
def get_all_moves(board, color, game):
    # store new board with piece moved to get to that board
    moves = []
    # loop through all pieces  in board of certain color
    for piece in board.get_all_pieces(color):
        # get all valid moves for each piece
        valid_moves = board.get_valid_moves(piece)
        # loop through dictinoary of items as key value pair
        # (Row, col) tuple: list of [pieces to skip]
        for move, skip in valid_moves.items():
            ## draw_moves(game, board, piece)
            # modify board to determine when moving to pos what new board looks like
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            # take piece, wanted move, temp board, and return new board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    # gets all valid moves for piece
    valid_moves = board.get_valid_moves(piece)
    # redraws board on game window
    board.draw(game.win)
    # green circle around piece on window
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    # draw all valid moves
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)