from creatures.base import Mammals
from utils import Color


class Herbivore(Mammals):
    def __init__(self, *args, **kwargs):
        super(Herbivore, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('YellowGreen')

    def eat(self, food):
        from predator import Predator
        from plant import Plant
        t = type(food)
        if t == Predator:
            if food.is_alive:
                food.health_down(10)
            else:
                food.health_down(1)
                self.health_down(1)
        elif t == Herbivore:
            if food.is_alive:
                food.health_down(10)
            else:
                food.health_down(1)
                self.health_down(1)
        elif t == Plant:
            food.health_down(10)
            self.health_up(10)

    def hunger(self):
        if self.turns % 2 == 0:
            self.health_down(1)