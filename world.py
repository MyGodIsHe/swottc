from OpenGL.GL import *
from OpenGL.GLUT import *
from utils import Color, Rectangle


class World(object):

    def __init__(self, cols, rows):
        self._objects = []
        self._field = []
        for x in xrange(cols):
            for y in xrange(rows):
                color = Color()
                color.set_bow(float(y)/rows)
                obj = Rectangle( (x - cols/2, y - rows/2, -15.0), color )
                self._objects.append(obj)
            self._field.append([ None for y in xrange(rows)])

    def add_creature(self, creature):
        self._objects.append(creature)
        self._field[creature.x][creature.y] = creature

    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # очищаем экран
        try:
            for obj in self._objects:
                obj.turn(self) #todo: need move to timer
                obj.draw()
        except:
            import traceback
            traceback.print_exc()
            sys.exit()
        glutSwapBuffers()

    def get_creature(self, x, y):
        return self._field[x][y]

    def move_creature(self, creature):
        pass