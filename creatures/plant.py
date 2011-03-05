from creatures.base import Base
from utils import Color


class Plant(Base):
    def __init__(self, *args, **kwargs):
        super(Plant, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color.by_name('YellowGreen')

    def turn(self, world):
        super(Plant, self).turn(world)

        if self.reproductive:
            self.reproductive -= 1
            self.health_up(1)

        if self.turns % 100 == 0:
            self.reproductive = self.base_health

    def aging(self):
        if self.turns % 10 == 0:
            self.health_down(1)