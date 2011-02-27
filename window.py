#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import logging
from utils import Color
from world import World
import settings


class Window(object):

    SIZE = 400, 400

    def __init__(self, log, colors, options):
        self.density = options.density
        self.cols = options.cols
        self.rows = options.rows
        self.is_force = False

        logging.basicConfig(filename=log, level=logging.DEBUG, filemode='w')

        Color.init(colors)

        self.background = Color.by_name('white').list()

        self.world = self.create_world()

        # set up pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # set up the window
        self.surface = pygame.display.set_mode(Window.SIZE, 0, 32)
        pygame.display.set_caption('Life')

        # set up fonts
        self.font = pygame.font.SysFont(None, 48)


    def create_world(self):
        from creatures import Predator, Herbivore, Plant

        if self.density < 1 or self.density > 100:
            sys.exit()
        world = World(cols=self.cols, rows=self.rows)
        cnt = int(world.cols * world.rows * 0.01 * self.density / 3)

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Predator(x=pos[0], y=pos[1])
            world.queue.append((i * 21, creature))

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Herbivore(x=pos[0], y=pos[1])
            world.queue.append((i * 22, creature))

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Plant(x=pos[0], y=pos[1])
            world.queue.append((i * 23, creature))

        world.start(0.1)
        return world


    def restart(self):
        World.clear_all()
        self.world = self.create_world()


    def rectangle(self, x, y, color):
        size = min(Window.SIZE) / max(self.world.cols, self.world.rows)
        rect = pygame.Rect(x * size, y * size, size, size)
        pygame.draw.rect(self.surface, color, rect)


    def key_pressed(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.world.stop()
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.world.stop()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r:
                    self.restart()
                elif event.key == K_f:
                    self.is_force = not self.is_force
                    if self.is_force:
                        self.world.begin_force()
                        print "Begin Force"
                    else:
                        self.world.end_force()
                        print "End Force"


    def loop(self):
        try:
            size = min(Window.SIZE) / max(self.world.cols, self.world.rows)
            dt = 0
            # run the game loop
            while True:
                # check for events
                self.key_pressed()

                # draw the black background onto the surface
                self.surface.fill(self.background)

                for obj in self.world._objects:
                    obj.update(dt)
                    obj.draw(self.surface, size)

                # draw the window onto the screen
                pygame.display.update()
                dt = self.clock.tick(settings.FPS)
        except:
            import traceback
            logging.debug(traceback.format_exc())
            self.world.stop()
            sys.exit()