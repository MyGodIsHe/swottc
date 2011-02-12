from utils import Timer
from OpenGL.GL import *
from OpenGL.GLUT import *
from constans import *


class World(object):
    worlds = []

    @staticmethod
    def clear_all():
        for world in World.worlds:
            world.stop()
        World.worlds = []

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self._objects = []
        self._field = []
        self._timer = None
        for x in xrange(cols):
            self._field.append([ None for y in xrange(rows)])

        World.worlds.append(self)

    def loop(self):
        try:
            for obj in self._objects:
                obj.turn(self)
        except:
            import traceback
            traceback.print_exc()
            self._timer.cancel()
            sys.exit()

    def start(self, speed):
        if self._timer:
            raise Exception()
        self._timer = Timer(speed, self.loop)
        self._timer.start()

    def stop(self):
        self._timer.cancel()

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
                self.rectangle(obj.x, obj.y, obj.color)
        except:
            import traceback
            traceback.print_exc()
            self._timer.cancel()
            sys.exit()
        glutSwapBuffers()

    def get_creature(self, x, y):
        if not self.check_position(x, y):
            return
        return self._field[x][y]

    def move_creature(self, creature):
        x, y = creature.x, creature.y
        if creature.course == COURSE_NORTH:
            x -= 1
        elif creature.course == COURSE_EAST:
            y += 1
        elif creature.course == COURSE_SOUTH:
            x += 1
        elif creature.course == COURSE_WEST:
            y -= 1
        if self.check_position(x, y):
            if self._field[x][y] is None:
                #todo: need lock
                self._field[creature.x][creature.y] = None
                self._field[x][y] = creature
                creature.x, creature.y = x, y

    def rectangle(self, x, y, color):
        glLoadIdentity()
        glTranslatef(x - self.cols/2, y - self.rows/2, -15.0)
        glColor4f(color.r, color.g, color.b, 1)
        size = 0.5
        glRectf(-size, -size, size, size)