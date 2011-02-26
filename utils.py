from threading import Thread, Event
from OpenGL.GL import *
from constans import *


class Color(object):
    MAX = 255
    MIN = 0
    color_by_name = {}

    @staticmethod
    def init(file_path):
        for i in open(file_path).readlines():
            i = i.split()
            if len(i) == 4:
                Color.color_by_name[i[3].lower()] = map(int, i[:3])

    @staticmethod
    def by_name(name):
        return Color(*Color.color_by_name[name.lower()])

    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return repr((self.r, self.g, self.b))

    def list(self):
        return (self.r, self.g, self.b)

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


def course_turn(course, is_r):
    if is_r:
        return COURSE_NORTH if course == COURSE_WEST else course + 1
    else:
        return COURSE_WEST if course == COURSE_NORTH else course - 1


class Timer(Thread):
    """Call a function after a specified number of seconds:

    t = Timer(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
        self.is_force = False

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        while not self.finished.is_set():
            if not self.is_force:
                self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)
        self.finished.set()