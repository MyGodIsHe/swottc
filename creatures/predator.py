from creatures.base import Mammals
from utils import Color


class Predator(Mammals):
    def __init__(self, *args, **kwargs):
        super(Predator, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('OrangeRed')

    def eat(self, creature):
        pass