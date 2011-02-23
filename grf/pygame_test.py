#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from sprite import spr_open
from actor import act_open


class Animation:

    def __init__(self, frames=None, time=100):
        self.frames = frames
        self.time = time
        self.work_time = 0
        self.skip_frame = 0
        self.frame = 0
        if type(time) == list:
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


def setup_animations(actor, sprites):
    animations = []

    for i in sprites:
        sprites.fill_rgba(i)
        i.data = ''.join(i.data)

    for animation in actor.animations:
        image_frames = []

        for frame in animation.frames:
            if frame.direction != 0:
                continue
            sprite = sprites[frame.image_n]
            sprite = pygame.image.fromstring(sprite.data,
                                             (sprite.width, sprite.height),
                                             'RGBA')
            sprite = pygame.transform.rotate(sprite, -frame.rotation)
            frame.sprite = sprite
            image_frames.append(frame)
        if len(image_frames):
            speed = animation.speed
            animations.append(Animation(image_frames, int(speed*40)))
    return animations


if __name__ == '__main__':
    pygame.init()

    display = pygame.display.set_mode((800, 600))

    screen = pygame.Surface(display.get_size())

    wolfs = setup_animations(act_open('wolf.act'), spr_open('wolf.spr'))
    wolfs = [w for i, w in enumerate(wolfs) if i % 4 == 0]

    clock = pygame.time.Clock()

    done = False
    dt = 0
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    done = True
                

        for wolf in wolfs:
            wolf.update(dt)

        screen.fill((255,255,255))

        y = 20
        for wolf in wolfs:
            frame = wolf.get_frame()
            screen.blit(frame.sprite, (50 + frame.offset_x, y + frame.offset_y))
            y += 100

        display.blit(screen,(0,0))
        pygame.display.flip()

        dt = clock.tick(40)