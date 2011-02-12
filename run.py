#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from world import World


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
    world = World(10, 10)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(400, 300)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Life")
    glutDisplayFunc(world.DrawGLScene)
    glutIdleFunc(world.DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(KeyPressed)
    InitGL(400, 300)
    glutMainLoop()

main()
