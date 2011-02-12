from creatures.base import Base


class Predator(Base):
    def __init__(self, position):
        super(Predator, self).__init__(position)
        self.base_health = 100
        self.current_health = self.base_health