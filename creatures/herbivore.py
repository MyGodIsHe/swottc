from creatures.base import Mammals
from utils import Color


class Herbivore(Mammals):
    def __init__(self, *args, **kwargs):
        super(Herbivore, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('YellowGreen')

    def eat(self, creature):
        pass