# https://www.youtube.com/playlist?list=PLzMcBGfZo4-lkJr3sqpikNyVzbNZLRiT3
import pygame
from checkers.constants import HEIGHT, SQUARE_SIZE, WIDTH
from checkers.game import Game

FPS = 60

# window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# take pos of mouse and output row/col
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    # constant frame rate
    clock = pygame.time.Clock()

    # start game
    game = Game(WIN)

    # main game loop
    while run:
        clock.tick(FPS)

        # print color to winner
        if game.winner() != None:
            print(game.winner())
            run = False

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # end while loop if quit
                run = False
            # press any button to check moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                # call select method
                game.select(row, col)

                # piece = board.get_piece(row, col)
                # board.move(piece, 4, 3)

        # draw board
        game.update()

    # quit pygame window
    pygame.quit()


main()
