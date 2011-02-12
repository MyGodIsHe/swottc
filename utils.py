from OpenGL.GL import *
from constans import *


class Color(object):
    MAX = 1.0
    MIN = 0.0

    def __init__(self, r=1.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return repr((self.r, self.g, self.b))

    def correct(self, c):
        if c > Color.MAX:
            return Color.MAX
        elif c < Color.MIN:
            return Color.MIN
        return c

    def set_bow(self, k):
        if k < Color.MIN or k > Color.MAX:
            raise Exception()
        c = int(6.0 * k)
        bow = [
            lambda k: (    Color.MAX, k / Color.MAX,     Color.MIN),
            lambda k: (k / Color.MAX,     Color.MAX,     Color.MIN),
            lambda k: (    Color.MIN,     Color.MAX, k / Color.MAX),
            lambda k: (    Color.MIN, k / Color.MAX,     Color.MAX),
            lambda k: (k / Color.MAX,     Color.MIN,     Color.MAX),
            lambda k: (    Color.MAX,     Color.MIN, k / Color.MAX),
        ]
        if c > 0:
            k = k % c
        self.r, self.g, self.b = bow[c](k)


    def up(self, step):
        if self.r == Color.MAX and Color.MIN <= self.g < Color.MAX and self.b == Color.MIN: # red
            self.g = self.correct(self.g + step)
        elif Color.MIN < self.r <= Color.MAX and self.g == Color.MAX and self.b == Color.MIN: # yellow
            self.r = self.correct(self.r - step)
        elif self.r == Color.MIN and self.g == Color.MAX and Color.MIN <= self.b < Color.MAX: # green
            self.b = self.correct(self.b + step)
        elif self.r == Color.MIN and Color.MIN < self.g <= Color.MAX and self.b == Color.MAX: # blue
            self.g = self.correct(self.g - step)
        elif Color.MIN <= self.r < Color.MAX and self.g == Color.MIN and self.b == Color.MAX: # blue
            self.r = self.correct(self.r + step)
        elif self.r == Color.MAX and self.g == Color.MIN and Color.MIN < self.b <= Color.MAX: # violet
            self.b = self.correct(self.b - step)
        else:
            raise Exception((self.r, self.g, self.b))


class Rectangle(object):
    def __init__(self, position=(0,0,0), color=Color()):
        self.x, self.y, self.z = position
        self.color = color

    def draw(self):
        glLoadIdentity()  # восстанавливаем мировые координаты
        glTranslatef(self.x, self.y, self.z)
        self.color.up(0.05)
        glColor4f(self.color.r, self.color.g, self.color.b, 1)
        size = 0.5
        glRectf(-size,-size,size,size)


def course_turn(course, is_r):
    if is_r:
        return COURSE_NORTH if course == COURSE_WEST else course + 1
    else:
        return COURSE_WEST if course == COURSE_NORTH else course - 1