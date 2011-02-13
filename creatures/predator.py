from creatures.base import Mammals
from utils import Color


class Predator(Mammals):
    def __init__(self, *args, **kwargs):
        super(Predator, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('OrangeRed')

    def eat(self, food):
        from herbivore import Herbivore
        from plant import Plant
        t = type(food)
        if t == Predator:
            if food.is_alive:
                food.health_down(20)
            else:
                food.health_down(10)
                self.health_up(10)
        elif t == Herbivore:
            if food.is_alive:
                food.health_down(50)
            else:
                food.health_down(25)
                self.health_up(25)
        elif t == Plant:
            food.health_down(1)
            self.health_down(1)