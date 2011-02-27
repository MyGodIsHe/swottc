import os
import pygame
from grf.actor import act_open
from grf.sprite import spr_open
import settings


class Animation(object):

    def __init__(self, frames, time=100):
        self.frames = frames
        self.time = time
        self.work_time = 0
        self.skip_frame = 0
        self.frame = 0
        if type(self.time) == list:
            self.__update = self.__update_any_time
        else:
            self.__update = self.__update_const_time

    def update(self, dt):
        self.work_time += dt
        self.__update(dt)

    def __update_const_time(self, dt):
        self.skip_frame = self.work_time / self.time
        if self.skip_frame > 0:
            self.work_time = self.work_time % self.time
            self.frame += self.skip_frame
            if self.frame >= len(self.frames):
                self.frame = 0

    def __update_any_time(self, dt):
        while self.work_time - self.time[self.frame] > 0:
            self.work_time -= self.time[self.frame]
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0

    def get_frame(self):
        return self.frames[self.frame]

    def draw(self, surface, x, y):
        for frame in self.get_frame():
            surface.blit(frame.sprite, (x + frame.offset_x, y + frame.offset_y))


class Actor(object):

    cache = {}

    @staticmethod
    def load(name):
        path = os.path.join(settings.ANIMATION_PATH, name)
        actor = act_open(path + '.act')
        sprites = spr_open(path + '.spr')

        animations = []

        for i in sprites:
            sprites.fill_rgba(i)
            i.data = ''.join(i.data)

        for animation in actor.animations:
            image_frames = []
            for subframes in animation.frames:
                image_subframes = []
                for frame in subframes:
                    sprite = sprites[frame.image_n]
                    sprite = pygame.image.fromstring(sprite.data,
                                                     (sprite.width, sprite.height),
                                                     'RGBA')
                    sprite = pygame.transform.rotate(sprite, -frame.rotation)
                    frame.sprite = sprite
                    image_subframes.append(frame)
                image_frames.append(image_subframes)
            speed = animation.speed
            animations.append((image_frames, speed))
        Actor.cache[name] = animations
        return animations

    def __init__(self, name):
        self.animations = Actor.cache.get(name)
        if not self.animations:
            self.animations = Actor.load(name)
        self.set_animation(0)

    def set_animation(self, n):
        self.current_animation = Animation(self.animations[n][0], int(self.animations[n][1]*settings.FPS))

    def draw(self, surface, size):
        self.current_animation.draw(surface, self.x * size, self.y * size)

    def update(self, dt):
        self.current_animation.update(dt)