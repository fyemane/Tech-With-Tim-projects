# https://www.youtube.com/watch?v=Q-__8Xw9KTM&t=851s
import pygame
import random
pygame.font.init()

# window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# load images
RED_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")

# player ship
YELLOW_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

# lasers
RED_LASER = pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

# background
BG = pygame.transform.scale(pygame.image.load(
    "assets/background-black.png"), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    # boolean if offscreen
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


# parent class
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        # class attributes
        self.x = x
        self.y = y
        self.health = health
        # will be images of objects
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        # prevents shooter spam
        self.cool_down_counter = 0

    def draw(self, window):
        # blit ship
        window.blit(self.ship_img, (self.x, self.y))

        # width gives hollow rect, filled in is nothing or 0
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))

        # draw lasers
        for laser in self.lasers:
            laser.draw(window)

    # move lasers for enemy
    # when moving lasers, check for collision with objs
    def move_lasers(self, vel, obj):
        # everytime laser moves, call once a frame
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # remove offscreen lasers
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # remove lasers that hit player
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # cooldown counter
    def cooldown(self):
        # if cooldown is 0, don't do anything
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        # if cooldown is not 0, increment by 1
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        # not in process of cooldown counting
        if self.cool_down_counter == 0:
            # create laser and add to list
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            # set cooldown counter to start counting up
            self.cool_down_counter = 1

    # get dimensions of image
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# inherits from ship class
class Player(Ship):
    def __init__(self, x, y, health=100):
        # super is parent class
        # use ship initialization class on ship
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # mask is array of image pixels
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # move lasers for player
    # when moving lasers, check for collision with objs
    def move_lasers(self, vel, objs):
        # everytime laser moves, call once a frame
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # remove offscreen lasers
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # remove lasers that hit enemy
            else:
                # for all active enemies
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        # if laser is in list, move it
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # draws parent draw and healthbar
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # red rect
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                         self.ship_img.get_width(), 10))
        # green rect
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                         self.ship_img.get_width() * (self.health/self.max_health), 10))


# class Enemy
class Enemy(Ship):
    # color dictionary with string matching enemy and laser color
    COLOR_MAP = {"red": (RED_SPACE_SHIP, RED_LASER),
                 "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                 "blue": (BLUE_SPACE_SHIP, BLUE_LASER)}

    def __init__(self, x, y, color, health=180):
        # super constructor - ship
        super().__init__(x, y, health)
        # use map to determine enemy color and laser
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        # not in process of cooldown counting
        if self.cool_down_counter == 0:
            # create laser and add to list
            laser = Laser(self.x - self.get_width()/2, self.y, self.laser_img)
            self.lasers.append(laser)
            # set cooldown counter to start counting up
            self.cool_down_counter = 1


# collide mask function
def collide(obj1, obj2):
    # distance between top left corners of objects to determine overlap
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # (x, y)


# main loop
def main():
    # dictate whether while loops runs
    run = True
    # checks for events/collision once every FPS
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    # list of enemies
    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    # initialize new player
    player = Player(300, 630)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # separate draw functions of classes/events into one function
    def redraw_window():
        # draws image as surface on window
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # draw enemies
        for enemy in enemies:
            enemy.draw(WIN)
        # draw player
        player.draw(WIN)

        # blit you lost at center of screen
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width() / 2,
                                  HEIGHT/2 - lost_label.get_height() / 2))

        # refresh display
        pygame.display.update()

    while run:
        # tick clock in every loop
        clock.tick(FPS)
        # blits bg and updates display
        redraw_window()

        # lose conditions
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            # don't do anything, go back to beginning of while loop and run
            else:
                continue

        # when enemies are gone, increment level and wave_length
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # create enemies and append to list
            for i in range(wave_length):
                # spawn enemies offscreen
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # check if user quits window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # returns dictionary of all keys and if pressed at given time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            # move 1 pixel to left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        # + 10 for healthbar
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # move enemies, make copy of enemy list to not modify looping list
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # probility that enemy shoots
            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            # player-enemy collision
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            # check enemy reaches bottom
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                # remove object from list
                enemies.remove(enemy)

        # check if player laser hits enemies
        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        # blit background and title screen
        WIN.blit(BG, (0, 0))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label,
                 (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))

        # event loop
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()
