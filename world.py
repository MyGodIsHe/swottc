from utils import Timer
from constans import *
import logging
from random import randint, choice


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
        self.queue = []
        for x in xrange(cols):
            self._field.append([ None for y in xrange(rows)])

        World.worlds.append(self)

    def check_queue(self):
        newqueue = []
        for turns, obj in self.queue:
            if turns == 0:
                self.add_creature(obj)
            else:
                newqueue.append((turns - 1, obj))
        return newqueue

    def loop(self):
        try:
            self.queue = self.check_queue()

            for obj in self._objects:
                obj.turn(self)
            deleted = filter(lambda obj: obj.is_nothing, self._objects)
            #todo: need lock
            for obj in deleted:
                logging.debug("Dead: %r, turns: %s, history: %s" % (obj, obj.turns, repr(obj.history.read())))
                self._field[obj.x][obj.y] = None
                self._objects.remove(obj)
            self.stabilize()
        except:
            import traceback
            logging.debug(traceback.format_exc())
            self._timer.cancel()

    def start(self, speed):
        if self._timer:
            raise Exception()
        self.init_count_objects = len(self._objects) + len(self.queue)
        self._timer = Timer(speed, self.loop)
        self._timer.start()

    def stop(self):
        self._timer.cancel()

    def begin_force(self):
        self._timer.is_force = True

    def end_force(self):
        self._timer.is_force = False

    def check_position(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def add_creature(self, creature):
        if not self.check_position(creature.x, creature.y):
            raise Exception()
        if self._field[creature.x][creature.y] is not None:
            return False
        self._objects.append(creature)
        self._field[creature.x][creature.y] = creature
        return True

    def add_creature_square(self, creature):
        if self.add_creature(creature): return True
        creature.x -= 1
        creature.y -= 1
        if self.add_creature(creature): return True
        creature.x += 1
        if self.add_creature(creature): return True
        creature.x += 1
        if self.add_creature(creature): return True
        creature.y += 1
        if self.add_creature(creature): return True
        creature.y += 1
        if self.add_creature(creature): return True
        creature.x -= 1
        if self.add_creature(creature): return True
        creature.x -= 1
        if self.add_creature(creature): return True
        creature.y -= 1
        if self.add_creature(creature): return True
        return False

    def get_rnd_free_space(self):
        free_cells = self.rows * self. cols - len(self._objects)
        n = randint(1, free_cells)
        if n == 0:
            return None
        for x in xrange(self.cols):
            for y in xrange(self.rows):
                if self._field[x][y] is None:
                    n -= 1
                    if n == 0:
                        return (x, y)
        return None

    def get_creature(self, x, y):
        if not self.check_position(x, y):
            return
        return self._field[x][y]

    def move_creature(self, creature):
        cell, pos = self.get_creature_by_course(creature)
        if cell is None and pos is not None:
            #todo: need lock
            self._field[creature.x][creature.y] = None
            self._field[pos[0]][pos[1]] = creature
            creature.x, creature.y = pos

    def get_creature_by_course(self, creature):
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
            return self._field[x][y], (x, y)
        return None, None

    def stabilize(self):
        crnt = len(self._objects) + len(self.queue)
        if crnt < self.init_count_objects:
            from creatures import Predator, Herbivore, Plant
            for i in xrange(self.init_count_objects - crnt):
                pos = self.get_rnd_free_space()
                if pos is None:
                    break
                cls = choice([Predator, Herbivore, Plant])
                creature = cls(x=pos[0], y=pos[1])
                self.add_creature(creature)