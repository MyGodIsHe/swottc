#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from creatures.herbivore import Herbivore
from creatures.plant import Plant
from creatures.predator import Predator
from utils import Color
from world import World
from random import randint


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
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


def ReSizeGLScene(Width, Height):
    if Height == 0: Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def KeyPressed(*args):
    if args[0]=="\033": sys.exit()


def main():
    Color.init('./rgb.txt')
    world = World(10, 10)

    for i in xrange(5):
        creature = Predator(x=randint(0, world.cols - 1),
                            y=randint(0, world.rows - 1))
        world.add_creature(creature)

    for i in xrange(5):
        creature = Herbivore(x=randint(0, world.cols - 1),
                             y=randint(0, world.rows - 1))
        world.add_creature(creature)

    for i in xrange(5):
        creature = Plant(x=randint(0, world.cols - 1),
                         y=randint(0, world.rows - 1))
        world.add_creature(creature)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(400, 300)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Life")
    glutDisplayFunc(world.draw_gl_scene)
    glutIdleFunc(world.draw_gl_scene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(KeyPressed)
    InitGL(400, 300)
    glutMainLoop()


if __name__ == '__main__':
    main()
