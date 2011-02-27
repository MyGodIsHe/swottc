from threading import Thread, Event
from constans import *


class Color:
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
        return Color.color_by_name[name.lower()]

    @staticmethod
    def by_html(bytes):
        return (int(bytes[0:2], 16),
                int(bytes[2:4], 16),
                int(bytes[4:6], 16))

    @staticmethod
    def correct(c):
        if c > Color.MAX:
            return Color.MAX
        elif c < Color.MIN:
            return Color.MIN
        return c

    @staticmethod
    def set_bow(k):
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
        return bow[c](k)

    @staticmethod
    def up(color, step):
        color = list(color)
        if color[0] == Color.MAX and Color.MIN <= color[1] < Color.MAX and color[2] == Color.MIN: # red
            color[1] = Color.correct(color[1] + step)
        elif Color.MIN < color[0] <= Color.MAX and color[1] == Color.MAX and color[2] == Color.MIN: # yellow
            color[0] = Color.correct(color[0] - step)
        elif color[0] == Color.MIN and color[1] == Color.MAX and Color.MIN <= color[2] < Color.MAX: # green
            color[2] = Color.correct(color[2] + step)
        elif color[0] == Color.MIN and Color.MIN < color[1] <= Color.MAX and color[2] == Color.MAX: # blue
            color[1] = Color.correct(color[1] - step)
        elif Color.MIN <= color[0] < Color.MAX and color[1] == Color.MIN and color[2] == Color.MAX: # blue
            color[0] = Color.correct(color[0] + step)
        elif color[0] == Color.MAX and color[1] == Color.MIN and Color.MIN < color[2] <= Color.MAX: # violet
            color[2] = Color.correct(color[2] - step)
        else:
            raise Exception(color)
        return tuple(color)


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