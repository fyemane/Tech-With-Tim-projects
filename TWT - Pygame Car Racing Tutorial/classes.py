import math, time
from utils import *

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        # whether or not current level started
        self.started = False
        # how much time elapsed in current level
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        # wait for user to start level
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    # determine if we have completed all levels
    def game_finished(self):
        return self.level > self.LEVELS

    # start level and level timer
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    # get time spent on current level
    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        # car not moving when starting
        self.vel = 0
        self.rotation_vel = rotation_vel
        # car starts at angle 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.2

    # pass True for either left/right to rotate
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    # draw the car image
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    # increase velocity of car based on accerlation, tops at terminal
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    # decrease velocity of car based on accerlation, tops at terminal
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    # move car
    def move(self):
        # trigonometry to move in 2D
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        # displacement between 2 masks
        offset = (int(self.x - x), int(self.y - y))
        # point of intersection
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

         
# specific player car inherits from abstract car
class PlayerCar(AbstractCar):
    IMG = RED_CAR 
    START_POS = (180, 200)

    # computer inherits from car class, does not need to slow down
    def reduce_speed(self):
        # slow down to 0, then stop
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    # car bounces if car hits wall
    def bounce(self):
        self.vel = -self.vel * .5
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    # override initialization
    def __init__(self, max_vel, rotation_vel, path=[]):
        # initilize needed values
        super().__init__(max_vel, rotation_vel)
        # path is list of coordinates for car to cross
        self.path = path
        # index of path list
        self.current_point = 0
        self.vel = max_vel

    # draws all points in the path
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    # override abstract draw method to draw computer car with points
    def draw(self, win):
        # abstract draw function
        super().draw(win)
        # draw all points in path
        # self.draw_points(win)

    # calculates the angle that leads to point
    def calculate_angle(self):
        # determine new target point
        target_x, target_y = self.path[self.current_point]
        # calc change in x,y
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        # calculate desired angle to turn, mitigate division by 0
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        # implement clause to refine angle if certain thing occurs?
        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        # make most efficient angle turn if angle diff is > 180
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # rotate current angle, prevents rotation_vel from passing desired angles
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += max(self.rotation_vel, abs(difference_in_angle))

    # move to next point in path
    def update_path_point(self):
        target = self.path[self.current_point]
        # image is a rect that doesn't know location
        # make rect using x,y of car with width/height of image
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        # use pygame to determine if point collides with rect
        if rect.collidepoint(*target):
            self.current_point += 1

    # determine how to move
    def move(self):
        # ensure we don't get index error by moving to non-existent point
        if self.current_point >= len(self.path):
            return

        # calculate angle and rotate car in angled direction
        self.calculate_angle()
        # check if to move to next point
        self.update_path_point()
        # get move function from abstract car
        super().move()

    # increasing computer speed after each level
    def next_level(self, level):
        self.reset()
        # speed factor
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0
 