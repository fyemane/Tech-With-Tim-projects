from classes import *

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)

TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 30)

# frames per second
FPS = 60

PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), 
        (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123),
       (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

def draw(win, images, player_car, computer_car, game_info):
    # blit each image in list
    for img, pos in images:
        win.blit(img, pos)

    # display stats
    level_text = MAIN_FONT.render(
        f"Level: {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()} s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)} px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_car.draw(win)
    computer_car.draw(win)
    # update display to show drawings
    pygame.display.update()

def move_player(player_car):
    # record key pressed
    keys = pygame.key.get_pressed()
    moved = False

    # rotate car left and right
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    # if not accelerating, slow down
    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car, game_info):
    # check collision with wall
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    # check collision with finish line for computer
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        # time in ms
        pygame.time.wait(5000)
        # reset game
        game_info.reset()
        # reset cars
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    # check collision with finish line for player
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            # increment next level for game info
            game_info.next_level()
            player_car.reset()
            # reset computer car and change speed for next level
            computer_car.next_level(game_info.level)

# main game loop
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0,0)),
         (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(2, 4, PATH)
game_info = GameInfo()

while run:
    # set processor speed
    clock.tick(FPS)

    # origin is top left
    draw(WIN, images, player_car, computer_car, game_info)

    # while not starting current level
    while not game_info.started:
        # starting screen
        blit_text_center(
            WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
        pygame.display.update()
        # check if user quits
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               break

           # if user presses key, exits start loop and starts level
           if event.type == pygame.KEYDOWN:
               game_info.start_level()

    # check if user quits
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
           break
        
       ## if mouse click, add mouse position to computer path list
       #if event.type == pygame.MOUSEBUTTONDOWN:
       #    pos = pygame.mouse.get_pos()
       #    computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.display.update()
        # time in ms
        pygame.time.wait(5000)
        # reset game
        game_info.reset()
        # reset cars
        player_car.reset()
        computer_car.reset()

pygame.quit()