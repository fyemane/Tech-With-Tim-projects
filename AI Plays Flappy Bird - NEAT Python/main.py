# https://github.com/techwithtim/NEAT-Flappy-Bird
import pygame
import neat
import time
import os
import random
import pickle
from classes import *
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730
DRAW_LINES = False
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

GEN = 0


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    for bird in birds:
        bird.draw(win)
    base.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gen: " + str(gen-1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render(
        "Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def main(genomes, config):
    global WIN, GEN
    win = WIN
    GEN += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        # sets up neural network for genome
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        # append bird object to list
        birds.append(Bird(230, 350))
        # append genome to list of genomes to track fitness
        g.fitness = 0
        ge.append(g)

    # setup window with initial conditions
    base = Base(FLOOR)
    pipes = [Pipe(700)]
    # set up clock
    clock = pygame.time.Clock()
    score = 0

    run = True
    # main game loop
    while run:
        # 30 ticks/s
        clock.tick(30)
        for event in pygame.event.get():
            # quits pygame
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        # set pipe index to 0, inputting first pipe
        pipe_ind = 0
        if len(birds) > 0:
            # if we pass first pipe, focus on 2nd pipe
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        # no birds left
        else:
            run = False
            break

        # pass values to neural network, get output value, check if value > 0.5, then jump
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate((bird.y,
                                      abs(bird.y - pipes[pipe_ind].height),
                                      abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        # move pipes and check collision
        for pipe in pipes:
            pipe.move()
            for x, bird in enumerate(birds):
                # everytime a bird hits pipe, removes 1 from fitness score
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # check if bird passes pipe and generate new pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # check if pipe is offscreen and add to removed list
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        # adds pipe and increases score
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        # remove deleted pipes
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            # checks if bird hit floor
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)

        # break if score gets large enough
        if score > 50:
            pickle.dump(nets[0], open("best.pickle", "wb"))
            break


def run(config_path):
    # define all the neat properties we set
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # generate a population
    p = neat.Population(config)

    # add a stats reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    # exact path to configuration
    config_path = os.path.join(local_dir, "AI.txt")
    run(config_path)
