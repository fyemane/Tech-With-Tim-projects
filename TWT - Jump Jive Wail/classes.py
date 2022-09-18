import pygame

screenWidth = 500
screenHeight = 480

# create a window with caption
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")
# set background
bg = pygame.image.load('bg.jpg')

class Player(object):
    walkRight = [pygame.image.load('player_imgs/R1.png'), pygame.image.load('player_imgs/R2.png'), pygame.image.load('player_imgs/R3.png'),
                pygame.image.load('player_imgs/R4.png'), pygame.image.load('player_imgs/R5.png'), pygame.image.load('player_imgs/R6.png'),
                pygame.image.load('player_imgs/R7.png'), pygame.image.load('player_imgs/R8.png'), pygame.image.load('player_imgs/R9.png')]
    walkLeft = [pygame.image.load('player_imgs/L1.png'), pygame.image.load('player_imgs/L2.png'), pygame.image.load('player_imgs/L3.png'),
                pygame.image.load('player_imgs/L4.png'), pygame.image.load('player_imgs/L5.png'), pygame.image.load('player_imgs/L6.png'),
                pygame.image.load('player_imgs/L7.png'), pygame.image.load('player_imgs/L8.png'), pygame.image.load('player_imgs/L9.png')]
    char = pygame.image.load('player_imgs/standing.png')

    # initialization function
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        # determines if player is jumping
        self.isJump = False
        self.left = False
        self.right = False
        # walkCount to iterate over sprites
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        # player hitbox
        self.hit_box = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        # draw character image
        # 9 sprites, 3 sprites per second, prevents index error
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
             
        if not self.standing:
            if self.left:
                # // excludes remainder
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        # if not moving, he is facing in last direction he was moving in
        else:
            # either standing in char frame, or in last frame
            # win.blit(char, (self.x, self.y))
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))

        # updated hit box
        self.hit_box = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0,), self.hit_box, 2)

    # player collides with goblin
    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        # reset jump
        self.isJump = False
        self.jumpCount = 10

        # show alert that player lost points
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenWidth / 2 - (text.get_width() / 2),
                       (screenHeight / 2 - (text.get_height() / 2))))
        pygame.display.update()

        # pauses game if we lose life
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            # makes sure we can exit game while game is paused
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # whether bullet is moving left/right
        self.facing = facing
        self.vel = 8 * facing

    # draw projectile
    def draw(self, win):
        # optional '1' means not filled in
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)

class Enemy(object):
    # class attributes
    walkRight = [pygame.image.load('enemy_imgs/R1E.png'), pygame.image.load('enemy_imgs/R2E.png'), pygame.image.load('enemy_imgs/R3E.png'),
                 pygame.image.load('enemy_imgs/R4E.png'), pygame.image.load('enemy_imgs/R5E.png'), pygame.image.load('enemy_imgs/R6E.png'),
                 pygame.image.load('enemy_imgs/R7E.png'), pygame.image.load('enemy_imgs/R8E.png'), pygame.image.load('enemy_imgs/R9E.png'),
                 pygame.image.load('enemy_imgs/R10E.png'), pygame.image.load('enemy_imgs/R11E.png')]
    walkLeft = [pygame.image.load('enemy_imgs/L1E.png'), pygame.image.load('enemy_imgs/L2E.png'), pygame.image.load('enemy_imgs/L3E.png'),
                pygame.image.load('enemy_imgs/L4E.png'), pygame.image.load('enemy_imgs/L5E.png'), pygame.image.load('enemy_imgs/L6E.png'),
                pygame.image.load('enemy_imgs/L7E.png'), pygame.image.load('enemy_imgs/L8E.png'), pygame.image.load('enemy_imgs/L9E.png'),
                pygame.image.load('enemy_imgs/L10E.png'), pygame.image.load('enemy_imgs/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        # start and end path of enemy
        self.path = [self.x, self.end]
        # counts our sprites
        self.walkCount = 0
        self.vel = 3
        self.hit_box = (self.x + 17, self.y + 2, 31, 57)
        # health
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            # moving right
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            # moving left
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # update enemy hitbox
            self.hit_box = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)

            # draw enemy health bars
            pygame.draw.rect(win, (255, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))

    # moves a certain path to an end position
    def move(self):
        # moving right
        if self.vel > 0:
            # check if character has reached path
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                # inverse velocity, change direction
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
