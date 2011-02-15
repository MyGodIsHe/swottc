#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except ImportError:
    print "Need install OpenGL"
    sys.exit()

import logging
from utils import Color
from world import World
from random import randint


class Window(object):

    def __init__(self, density):
        self.density = density

        LOG_FILENAME = 'debug.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w')

        Color.init('./rgb.txt')

        self.world = self.create_world()

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(400, 300)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("Life")
        glutDisplayFunc(self.world.draw_gl_scene)
        glutIdleFunc(self.world.draw_gl_scene)
        glutReshapeFunc(self.ReSizeGLScene)
        glutKeyboardFunc(self.KeyPressed)
        self.InitGL(400, 300)


    def InitGL(self, Width, Height):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)


    def ReSizeGLScene(self, Width, Height):
        if Height == 0: Height = 1
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def KeyPressed(self, *args):
        if args[0]=="\033":
            self.world.stop()
            sys.exit()
        elif args[0]=="\x12":
            self.restart()


    def create_world(self):
        from creatures import Predator, Herbivore, Plant

        if self.density < 1 or self.density > 100:
            sys.exit()
        world = World(cols=50, rows=50)
        cnt = int(world.cols * world.rows * 0.01 * self.density)

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Predator(x=pos[0], y=pos[1])
            world.add_creature(creature)

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Herbivore(x=pos[0], y=pos[1])
            world.add_creature(creature)

        for i in xrange(cnt):
            pos = world.get_rnd_free_space()
            if pos is None:
                break
            creature = Plant(x=pos[0], y=pos[1])
            world.add_creature(creature)

        world.start(0.1)
        return world


    def restart(self):
        World.clear_all()
        self.world = self.create_world()
        glutDisplayFunc(self.world.draw_gl_scene)
        glutIdleFunc(self.world.draw_gl_scene)


    def loop(self):
        glutMainLoop()


if __name__ == '__main__':
    window = Window(density=3)
    window.loop()