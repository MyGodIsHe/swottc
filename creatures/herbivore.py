from creatures.base import Mammals
from utils import Color


class Herbivore(Mammals):
    def __init__(self, *args, **kwargs):
        super(Herbivore, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('DarkSlateBlue')

    def eat(self, food):
        from predator import Predator
        from plant import Plant
        t = type(food)
        if t == Predator:
            if food.is_alive:
                ch, bh = food.health_down(10)
                self.history.append("Hit predator (%s)" % ch)
            else:
                ch, bh = food.health_down(1)
                self.health_down(bh)
                self.history.append("Eat predator (%s)" % bh)
        elif t == Herbivore:
            if food.is_alive:
                ch, bh = food.health_down(10)
                self.history.append("Hit herbivore (%s)" % ch)
            else:
                ch, bh = food.health_down(1)
                self.health_down(bh)
                self.history.append("Eat herbivore (%s)" % bh)
        elif t == Plant:
            ch, bh = food.health_down(10)
            hp = self.health_up(ch or bh)
            self.reproductive_up(hp)
            self.history.append("Eat plant (%s)" % hp)

    def hunger(self):
        if self.turns % 2 == 0:
            self.health_down(1)