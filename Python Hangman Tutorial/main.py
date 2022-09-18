# https://www.youtube.com/playlist?list=PLzMcBGfZo4-ndZlN21DasvpfKwIc1rI6w
import pygame
import math
import random

# initialize
pygame.init()

# setup display and screen dimensions
WIDTH, HEIGHT = 800, 500
# function accepts tuple
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# buttom variables
RADIUS = 20
GAP = 15
# letters values have (x, y, ltr, boolean)
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
# in computing, every character defined by number
A = 65
# x,y of each circle
for i in range(26):
    # x for each circle
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + (i // 13) * (GAP + RADIUS * 2)
    # append pairs of x,y values into list
    # character representation of 65 + i
    # True means button is visible
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 30)
WORD_FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)


# load images
images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    images.append(image)

# game variables
hangman_status = 0
words = ["DEVELOPER", "HELLO", "PYTHON", "PYGAME", "IDE", "REPLIT"]
word = random.choice(words)
# letters guessed so far
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw():
    # fill window with white
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        # check if letter is in guessed
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        # unpacking
        x, y, ltr, visible = letter
        # check if button is visible
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            # draw letter
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    # draw hangman image
    win.blit(images[hangman_status], (150, 100))
    # update display
    pygame.display.update()


# display message
def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width() / 2,
                    HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    # global var accessible inside loop
    global hangman_status
    # setup game loop
    FPS = 60
    # clock object to set main loop at speed
    clock = pygame.time.Clock()
    run = True

    while run:
        # tick at speed
        clock.tick(FPS)

        # check for events
        for event in pygame.event.get():
            # check if user quits
            if event.type == pygame.QUIT:
                run = False
            # check for mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    # find distance btwn position of letter and mouse
                    x, y, ltr, visible = letter
                    if visible:
                        distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        # if mouse pos within button
                        if distance < RADIUS:
                            # edit actual letter variable to be invisible
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        # draw before end screen
        draw()

        # user wins if all letters in word are in guessed
        won = True
        for letter in word:
            if letter not in guessed:
                # won stays True if word completely guessed
                won = False
                break
        if won:
            display_message("You WON!")
            break
        # if stickman complete, game over
        if hangman_status == 6:
            display_message("You LOST!")
            break

main()

# close window
pygame.quit()
