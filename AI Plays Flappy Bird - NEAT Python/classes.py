import pygame
import time
import os
import random

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    # how much the bird tilts
    MAX_ROTATION = 25
    # how much to rotate on each frame or move bird
    ROT_VEL = 20
    # how long to show each bird animation (how fast bird flaps)
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        # physics of bird to jump/fall
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        # when we last jump
        self.tick_count = 0
        self.height = self.y

    # every frame to move
    def move(self):
        # time unit
        self.tick_count += 1
        # parabolic displacement - # pixels moving up
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        # terminal velocity
        if d >= 16:
            d = 16
        # jump to be higher/lower
        if d < 0:
            d -= 2 
        # add d to current y position
        self.y += d

        # moving upwards or every time we jump we keep track of initial height
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # tilting bird down
            if self.tilt > -90:
                # rotates bird completely 90, nosedives
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        # how many times have we shown one image
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            # display first image
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            # display 2nd image
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            # display last image
            self.img = self.IMGS[2] 
        elif self.img_count <= self.ANIMATION_TIME*4:
            # display 2nd image
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            # display 1st image and reset
            self.img = self.IMGS[0]
            self.img_count = 0

        # if nosedives, stop flapping
        if self.tilt <= -90:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # makes rotated image
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    # space between pipe
    VEL = 5
    GAP = 200

    def __init__(self, x):
        self.x = x
        self.height = 0

        # tracks top and bottom of pipe
        self.top = 0
        self.bottom = 0
        # images of pipes have to be flipped
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        # collision
        self.passed = False
        # defines where the top and bottom of pipes are and their height
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        # sets height for top pipe relative to top left corner of image
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    # moves the pipe
    def move(self):
        self.x -= self.VEL

    # draws pipe (pipe is both top and bottom pipe)
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # pixel perfect collision mechanic using mask comparing pixel overlap
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # how far away the two top left and bottom left masks are from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # point of overlap between bird mask and bottom pipe, returns None if no collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # checks for collision
        if t_point or b_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # each bg image moves left
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # when each image is offscreen on the left, immediately cycles back
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)