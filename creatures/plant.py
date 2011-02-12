from creatures.base import Base
from utils import Color


class Plant(Base):
    def __init__(self, *args, **kwargs):
        super(Plant, self).__init__(*args, **kwargs)
        self.base_health = 100
        self.current_health = self.base_health
        self.color = Color().by_name('Gold')