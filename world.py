from OpenGL.GL import *
from OpenGL.GLUT import *


class World(object):

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self._objects = []
        self._field = []
        for x in xrange(cols):
            self._field.append([ None for y in xrange(rows)])

    def check_position(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def add_creature(self, creature):
        if not self.check_position(creature.x, creature.y):
            return False
        if self._field[creature.x][creature.y] is not None:
            return False
        self._objects.append(creature)
        self._field[creature.x][creature.y] = creature
        return True

    def draw_gl_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        try:
            for obj in self._objects:
                obj.turn(self) #todo: need move to timer
                self.rectangle(obj.x, obj.y, obj.color)
        except:
            import traceback
            traceback.print_exc()
            sys.exit()
        glutSwapBuffers()

    def get_creature(self, x, y):
        if not self.check_position(x, y):
            return
        return self._field[x][y]

    def move_creature(self, creature):
        pass

    def rectangle(self, x, y, color):
        glLoadIdentity()
        glTranslatef(x - self.cols/2, y - self.rows/2, -15.0)
        glColor4f(color.r, color.g, color.b, 1)
        size = 0.5
        glRectf(-size, -size, size, size)