from random import choice
from neurons import Kohonen
from constans import *
from utils import course_turn


class CreatureType(object):
    def __init__(self, predators=0, herbivores=0, plants=0):
        self.predators = predators
        self.herbivores = herbivores
        self.plants = plants


class Eye(object):
    """ F F F
        L A R
        L * R
    """

    north = (
        ( (-1, -2), ( 0, -2), ( 1, -2) ), # F
        ( (-1, -1), (-1, 0) ),            # L
        ( ( 1, -1), ( 1, 0) ),            # R
        ( ( 0, -1), ),                    # A
    )
    east = (
        ( ( 2,  -1), ( 2,  0), ( 2,  1) ),
        ( ( 0, -1), ( 1, -1) ),
        ( ( 0,  1), ( 1,  1) ),
        ( ( 1,  0), ),
    )
    south = (
        ( (-1,  2), ( 0,  2), ( 1,  2) ),
        ( ( 1,  0), ( 1,  1) ),
        ( (-1,  0), (-1,  1) ),
        ( ( 0,  1), ),
    )
    west = (
        ( (-2,  1), (-2,  0), (-2,  -1) ),
        ( ( 0,  1), (-1,  1) ),
        ( ( 0, -1), (-1, -1) ),
        ( (-1,  0), ),
    )

    def __init__(self, course, world, position):
        from herbivore import Herbivore
        from plant import Plant
        from predator import Predator
        self.front = CreatureType()
        self.left = CreatureType()
        self.right = CreatureType()
        self.action = CreatureType()

        array = { COURSE_NORTH: Eye.north,
                  COURSE_EAST: Eye.east,
                  COURSE_SOUTH: Eye.south,
                  COURSE_WEST: Eye.west,
        }[course]

        for xys, place in zip(array, [self.front, self.left, self.right, self.action]):
            for xy in xys:
                creature = world.get_creature(position[0] + xy[0], position[1] + xy[1])
                if isinstance(creature, Predator):
                    place.predators += 1
                elif isinstance(creature, Herbivore):
                    place.herbivores += 1
                elif isinstance(creature, Plant):
                    place.plants += 1


class Base(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turns = 0

    def turn(self, world):
        self.turns += 1


class Mammals(Base):
    def __init__(self, *args, **kwargs):
        super(Mammals, self).__init__(*args, **kwargs)
        self.brain = Kohonen(12, 6, 4)
        self.course = choice((COURSE_SOUTH, COURSE_NORTH, COURSE_WEST, COURSE_EAST))
        self.turns = 0

    def turn(self, world):
        super(Mammals, self).turn(world)
        eye = Eye(self.course, world, (self.x, self.y))
        answer = self.brain.signal_eye(eye)
        if ACTION_GO == answer:
            world.move_creature(self)
        elif ACTION_LEFT == answer:
            self.course = course_turn(self.course, False)
        elif ACTION_RIGHT == answer:
            self.course = course_turn(self.course, True)
        elif ACTION_EAT == answer:
            self.eat(creature)
        else:
            raise Exception()

    def eat(self):
        raise Exception("Need to implement")