# https://www.youtube.com/playlist?list=PLzMcBGfZo4-krMMJ2EPdVzsOCJDoe0K-I
from typing import ChainMap
import pygame
import random

from pygame.constants import KEYDOWN

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

# top left position of play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
# select shapes by indexing on list
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


# main data structure for piece
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # locked_positions is dictionary of locations with color
    # 10x20 grid by list full of colors
    # create a list for every row in grid
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    # draw pieces already in grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # j is x value (col), i is y value (row)
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


# input shape format and output
def convert_shape_format(shape):
    # generate list of positions to check, draw, etc.
    positions = []
    # if current rotation is 0 -> len=4 -> first shape
    format = shape.shape[shape.rotation % len(shape.shape)]

    # look through every row/col for 0 or .
    for i, line in enumerate(format):
        row = list(line)
        # in every row, get current line and check for 0 or .
        for j, col in enumerate(row):
            if col == '0':
                # add x, y value for 0 place, relative to shape's current position
                positions.append((shape.x + j, shape.y + i))
    # remove trailing periods, offset to right/down by too much
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# check grid to see if moving to valid space
def valid_space(shape, grid):
    # every single position in 10x20 grid and adding as tuple into var
    # only add position into accepted posiiton if empty
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                    for i in range(20)]
    # flatten list (convert to 1D)
    accepted_pos = [j for sub in accepted_pos for j in sub]
    # formatted shape
    formatted = convert_shape_format(shape)
    # check if pos is in accepted_pos
    for pos in formatted:
        if pos not in accepted_pos:
            # when removing offset, they may spawn abovescreen
            # only ask for valid position if >= 0
            if pos[1] > -1:
                return False
    return True


# check if any position are above the screen
# if piece above screen, lost game
def check_lost(positions):
    # pass list of positions
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    # if every position's y < 1, lost game
    return False


def get_shape():
    # outputs random shape
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    # middile position
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2,
                         top_left_y + play_height/2 - label.get_height()/2))


# draw grid structure
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # draw lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    increment = 0
    # in dictionary if change key that already exist, overrides key
    # loop through grid backwards at bottom to mitigate this
    for i in range(len(grid) - 1, -1, -1):
        # set row to every row in grid
        row = grid[i]
        # if there is no black square in row, then completely filled
        if (0, 0, 0) not in row:
            # get every position in row
            # increase increment to shift it down another row
            increment += 1
            index = i
            # loop through j in row, i stays static
            for j in range(len(row)):
                try:
                    # locked positions need to be removed
                    # change locked as is mutable dictionary
                    # delete keys and colors from grid
                    # delete row at bottom and add empty row on top of grid
                    # then update grid so it appears to shift down
                    del locked[(j, i)]
                except:
                    continue

    if increment > 0:
        # for every key in sorted list of locked positions
        # sort list by y value
        # get all positions with same y value in correct order
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # shift every position in grid down
            if y < index:
                # if y value is above current index of row removed, then only blocks above shifted
                newKey = (x, y + increment)
                # create new key in locked position with same color as last key but
                # it's equal to this position
                locked[newKey] = locked.pop(key)

    # number of rows cleared
    return increment


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    # position to the right of grid
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    # get sublist
    format = shape.shape[shape.rotation % len(shape.shape)]

    # drawing blocks according to where they show up in list
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j*block_size + 20, sy + i*block_size + 20,
                                  block_size, block_size), 0)

    # blit the label
    surface.blit(label, (sx + 10, sy - 30))


def update_score(n_score):
    # open text file
    score = max_score()
    with open("scores.txt", 'w') as f:
        # if current score is greater than high score
        if int(score) > n_score:
            f.write(str(score))
        else:
            f.write(str(n_score))


def max_score():
    with open("scores.txt", 'r') as f:
        lines = f.readlines()
        # score is first line, remove \n
        score = lines[0].strip()
    return score


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    # initialize font
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    # blit on middle of screen
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    # current score text
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render(f"Score: {score}", 1, (255, 255, 255))
    # position to draw score
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 30, sy + 160))

    # high score text
    label = font.render(f"High Score: {last_score}", 1, (255, 255, 255))
    # position to draw high score
    sx = top_left_x + play_width - 10
    sy = top_left_y + play_height/2 - 50
    surface.blit(label, (sx + 30, sy + 160))

    # drawing all grid objects on screen
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*block_size, top_left_y + i*block_size,
                              block_size, block_size), 0)
    # draw red rect
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)
    # pygame.display.update()


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    # outputs random shape
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    # game loop
    while run:
        # everytime we move, we have chance to add something to locked_positions
        # if we hit screen bottom, locked_positions will haven new shape
        # constantly update grid
        grid = create_grid(locked_positions)
        # how long since last loop ran
        # rawtime gets amout of time since last clock.tick()
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # every x seconds, increase speed
        if level_time/1000 > 5:
            level_time = 0
            # change speed
            if fall_speed > 0.12:
                # change rate of speed change
                fall_speed -= 0.005

        # piece automatically moves down
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # check if moved space is valid and not at top of screen
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # either hit bottom of screen or hit piece
                # stop moving piece and change it
                change_piece = True

        for event in pygame.event.get():
            # if user qutis
            if event.type == pygame.QUIT:
                run = False
            # main controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current_piece.x -= 1
                    # check if valid position
                    if not valid_space(current_piece, grid):
                        # move back as if it wasn't moved
                        current_piece.x += 1
                if event.key == pygame.K_d:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_s:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_w:
                    # rotate shape
                    current_piece.rotation += 1
                    # check if invalid rotat ion
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        # check all positions of piece moving down to see if hit ground or lock
        shape_pos = convert_shape_format(current_piece)

        # add piece's color to grid to see piece drawed
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            # if not abovescreen
            if y > -1:
                # grid stores colors, draw color based on shape's position
                grid[y][x] = current_piece.color

        # when passing locked_positions in grid, get each position, then update grid color
        # if piece hit bottom
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # locked positions is dictionary of tuples - (x,y):(R,G,B)
                locked_positions[p] = current_piece.color
            # move to next piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # clear rows after piece is static and change score
            score += clear_rows(grid, locked_positions) * 10

        # draw new grid on window
        draw_window(win, grid, score, last_score)
        # draw next shape
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # if user lost
        if check_lost(locked_positions):
            # display "YOU LOST" text
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press Any Key To Play", 60, (255, 255, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            # start game
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


# create window
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris!")
main_menu(win)  # start game
