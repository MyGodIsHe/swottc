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

    SIZE = 800, 800
    CELL_SIZE = 60

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
        self.world_surface = pygame.Surface((self.cols * Window.CELL_SIZE, self.rows * Window.CELL_SIZE))

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
        self.is_force = False
        self.world = self.create_world()


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
            dt = 0
            # run the game loop
            while True:
                # check for events
                self.key_pressed()

                # draw the black background onto the surface
                self.world_surface.fill(self.background)

                for obj in self.world._objects:
                    obj.update(dt)
                    obj.draw(self.world_surface, Window.CELL_SIZE)

                cursize = Window.SIZE
                scaled_surf = pygame.transform.smoothscale(self.world_surface, cursize)
                self.surface.fill(self.background)
                scaled_surf_pos = scaled_surf.get_rect(centerx=Window.SIZE[0]/2, centery=Window.SIZE[1]/2)
                self.surface.blit(scaled_surf, scaled_surf_pos)
                pygame.display.flip()

                # draw the window onto the screen
                #pygame.display.update()

                dt = self.clock.tick(settings.FPS)
        except:
            import traceback
            logging.debug(traceback.format_exc())
            self.world.stop()
            sys.exit()