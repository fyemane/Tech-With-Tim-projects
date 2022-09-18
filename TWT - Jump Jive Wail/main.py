from classes import *

# initialise pygame
pygame.init()

# controls FPS
clock = pygame.time.Clock()

# sounds
bulletSound = pygame.mixer.Sound('laser_shot.wav')
hitSound = pygame.mixer.Sound('explosion.wav')
# loop music
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# score
score = 0

# redraw game window
def redraw_game_window():
    # fill with picture
    win.blit(bg, (0, 0))
    # renders new text ready to be put on the screen
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (480 - text.get_width(), 10))
    # draw man
    man.draw(win)
    # draw goblin
    goblin.draw(win)
    # draw bullets
    global bullet
    for bullet in bullets:
        bullet.draw(win)
    # refresh the display
    pygame.display.update()

# draw text
font = pygame.font.SysFont('comicsans', 30, True)

# create objects
man = Player(200, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []

# main game loop
run = True
while run:
    # sets FPS
    clock.tick(27)

    if goblin.visible:
        # checking collision of bullet and goblin
        if man.hit_box[1] < goblin.hit_box[1] + goblin.hit_box[3] and man.hit_box[1] + man.hit_box[3] > goblin.hit_box[1]:
            if man.hit_box[0] + man.hit_box[2] > goblin.hit_box[0] and man.hit_box[0] < goblin.hit_box[0] + goblin.hit_box[2]:
                man.hit()
                score -= 5

    # bullet cooldown
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    # get and check list of all events
    for event in pygame.event.get():
        # if click exit button
        if event.type == pygame.QUIT:
            run = False

    # bullet operations
    for bullet in bullets:
        # checking collision of bullet and goblin
        # if bullet is between top and bottom of goblin's hitbox
        if bullet.y - bullet.radius < goblin.hit_box[1] + goblin.hit_box[3] and bullet.y + bullet.radius > goblin.hit_box[1]:
            # if bullet is between left and right of hitbox
            if bullet.x + bullet.radius > goblin.hit_box[0] and bullet.x - bullet.radius < goblin.hit_box[0] + goblin.hit_box[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        # not going offscreen
        if 0 < bullet.x < 500:
            # bullet is shot
            bullet.x += bullet.vel
        else:
            # find index of unwanted bullet in list and delete it
            bullets.pop(bullets.index(bullet))

    # set list of key presses and constraints inside window
    keys = pygame.key.get_pressed()

    # shooting mechanism
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        # direction that bullet appears
        if man.left:
            facing = -1
        else:
            facing = 1
        # sets number of bullets that can appear
        if len(bullets) < 5:
            # add bullets to list, bullet comes out from middle of man
            bullets.append(Projectile(round(man.x + man.width // 2), 
                                      round(man.y + man.height // 2), 
                                      6, (0, 0, 0), facing))
        # shoot bullets one at a time
        shootLoop = 1

    # boundary checking and setting motion
    if keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_d] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    # jumping algorithm
    if not man.isJump:
        if keys[pygame.K_w]:
            # not moving if jumping
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            # neg variable for object to move downward
            neg = 1
            # if jumpCount < 0, start falling down
            if man.jumpCount < 0:
                neg = -1
            # quadratic equation to jump
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            # decrease velocity up
            man.jumpCount -= 1
        else:
            # reset jump variable back to initial
            man.isJump = False
            man.jumpCount = 10

    redraw_game_window()

# ends program and closes window
pygame.quit()
