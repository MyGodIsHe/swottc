from random import choice
from neurons import Kohonen
from constans import *
from utils import course_turn
from random import choice
import logging


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

        self.creature = []

        for xys, place in zip(array, [self.front, self.left, self.right, self.action]):
            for xy in xys:
                creature = world.get_creature(position[0] + xy[0], position[1] + xy[1])
                t = type(creature)
                if t == Predator:
                    place.predators += 1
                    self.creature.append(creature)
                elif t == Herbivore:
                    place.herbivores += 1
                    self.creature.append(creature)
                elif t == Plant:
                    place.plants += 1
                    self.creature.append(creature)


class History(object):
    def __init__(self, creature):
        self.events = []
        self.creature = creature

    def append(self, message):
        self.events.append("Turn: %s, Message: %s" % (self.creature.turns, message))

    def read(self):
        return repr(self.events)


class Base(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turns = 0
        self.history = History(self)
        self.reproductive = 0

    def turn(self, world):
        self.turns += 1

    def health_up(self, hp):
        if self.current_health + hp > self.base_health:
            up_hp = self.base_health - self.current_health
            self.current_health = self.base_health
        else:
            up_hp = hp
            self.current_health += hp
        return up_hp

    def _base_health_down(self, hp):
        if self.base_health > 0:
            if hp > self.base_health:
                hp_down = self.base_health
                self.base_health = 0
            else:
                hp_down = hp
                self.base_health -= hp
        else:
            hp_down = 0
        return hp_down

    def health_down(self, hp):
        if self.current_health > 0:
            if hp > self.current_health:
                ch_down = self.current_health
                self.current_health = 0
                bh_down = self._base_health_down(hp - ch_down)
            else:
                ch_down = hp
                self.current_health -= hp
                bh_down = 0
        else:
            ch_down = 0
            bh_down = self._base_health_down(hp)
        return ch_down, bh_down

    @property
    def is_nothing(self):
        return self.base_health == 0

    @property
    def is_alive(self):
        return self.current_health > 0


class Mammals(Base):
    def __init__(self, *args, **kwargs):
        super(Mammals, self).__init__(*args, **kwargs)
        self.brain = Kohonen(12, 6, 4)
        self.course = choice((COURSE_SOUTH, COURSE_NORTH, COURSE_WEST, COURSE_EAST))
        self.turns = 0

    def turn(self, world):
        super(Mammals, self).turn(world)
        if not self.is_alive:
            return
        eye = Eye(self.course, world, (self.x, self.y))
        if self.is_ready_reproduction:
            self.reproduction(eye.creatures, world)
        answer = self.brain.signal_eye(eye)
        if ACTION_GO == answer:
            world.move_creature(self)
        elif ACTION_LEFT == answer:
            self.course = course_turn(self.course, False)
        elif ACTION_RIGHT == answer:
            self.course = course_turn(self.course, True)
        elif ACTION_EAT == answer:
            creature, pos = world.get_creature_by_course(self)
            if creature:
                self.eat(creature)
        else:
            raise Exception()
        self.hunger()

    def eat(self):
        raise Exception("Need to implement")

    def hunger(self):
        raise Exception("Need to implement")

    def reproduction(self, creatures, world):
        variants = filter(lambda x: isinstance(x, self.__class__) and x.is_ready_reproduction, creatures)
        if variants:
            partner = choice(variants)
            partner.reproductive = 0
            self.reproductive = 0
            child = self.__class__(x=self.x, y=self.y)
            child.brain = Kohonen.generate(child.brain, self.brain, partner.brain)
            is_add = world.add_creature_square(child)
            self.history.append("Birth %s %s" % (is_add, child))

    def reproductive_up(self, hp):
        if self.reproductive + hp > self.base_health:
            self.reproductive = self.base_health
        else:
            self.reproductive += hp

    @property
    def is_ready_reproduction(self):
        return self.reproductive == self.base_health