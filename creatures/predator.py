from creatures.base import Mammals
from utils import Color


class Predator(Mammals):
    def __init__(self, *args, **kwargs):
        super(Predator, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color.by_name('OrangeRed')

    def eat(self, food):
        from herbivore import Herbivore
        from plant import Plant
        t = type(food)
        if t == Predator:
            if food.is_alive:
                ch, bh = food.health_down(20)
                self.history.append("Hit predator (%s)" % ch)
            else:
                ch, bh = food.health_down(10)
                hp = self.health_up(bh)
                self.reproductive_up(hp)
                self.history.append("Eat predator (%s)" % hp)
        elif t == Herbivore:
            if food.is_alive:
                ch, bh = food.health_down(50)
                self.history.append("Hit herbivore (%s)" % ch)
            else:
                ch, bh = food.health_down(25)
                hp = self.health_up(bh)
                self.reproductive_up(hp)
                self.history.append("Eat herbivore (%s)" % hp)
        elif t == Plant:
            ch, bh = food.health_down(1)
            self.health_down(ch or bh)
            self.history.append("Eat plant (%s)" % 1)

    def hunger(self):
        if self.turns % 10 == 0:
            self.health_down(1)
