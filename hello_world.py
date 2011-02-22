#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyglet
from pyglet.window import mouse


def get_row(cols):
    prevx = cols[0]
    items = []
    for col in cols[1:]:
        items.append((prev, y, col - prev, h))
        prev = col
    return items


def setup_animation(img, positions):
    base_image = pyglet.image.load(img)
    image_frames = []

    for x, y, w, h in positions:
        frame = base_image.get_region(x=x, y=y, width=w, height=h)
        animation_frame = (pyglet.image.AnimationFrame(frame, 0.2))
        image_frames.append(animation_frame)

    animation = pyglet.image.Animation(image_frames)
    return animation


window = pyglet.window.Window(800, 600, resizable=True)
scale = 1.0
camera_x = 0.0
camera_y = 0.0
label_fps = pyglet.text.Label('FPS',
                              font_name='Times New Roman',
                              font_size=12,
                              x=795, y=5,
                              anchor_x='left', anchor_y='top')

positions = [(92, 67), (80, 66), (95, 56),
             (77, 75), (84, 61), (78, 60),
             (67, 61), (76, 62), (75, 65), (75, 61), (76, 60),
             (67, 65), (66, 70), (66, 71), (68, 74), (68, 66),
             (67, 61), (70, 57), (72, 54), (106, 51), (81, 68),
             (52, 92), (75, 66), (69, 67), (72, 62), (73, 58),
             (81, 78), (72, 72), (62, 75), (72, 62), (67, 61),
             (70, 65), (69, 67), (72, 71), (69, 75), (61, 71),
             (81, 64), (79, 68), (80, 71), (99, 68), (67, 58),
             (72, 59), (68, 63), (68, 63)]


drawableObjects = []
drawableObjects.append(pyglet.sprite.Sprite(
    x=0, y=0,
    img=setup_animation(u'./Картинки/wolf.png', get_row(positions[:3]))))
drawableObjects.append(pyglet.sprite.Sprite(
    x=107, y=0,
    img=setup_animation(u'./Картинки/wolf.png', get_row(positions[3:6]))))
drawableObjects.append(pyglet.sprite.Sprite(
    x=214, y=0,
    img=setup_animation(u'./Картинки/wolf.png', get_row(positions[6:11]))))
drawableObjects.append(pyglet.sprite.Sprite(
    x=299, y=0,
    img=setup_animation(u'./Картинки/wolf.png', get_row(positions[11:16]))))

drawableObjects = [(i.x, i.y, i) for i in drawableObjects]


@window.event
def on_draw():
    global camera_x, camera_y
    window.clear()
    for x, y, i in drawableObjects:
        i.scale = scale
        i.x = x + (window.width//2 - camera_x - x) * (1 - scale) + camera_x
        i.y = y + (window.height//2 - camera_y - y) * (1 - scale) + camera_y
        i.draw()
    label_fps.draw()


@window.event
def on_resize(width, height):
    print 'The window was resized to %dx%d' % (width, height)


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scale
    if scroll_y > 0:
        scale *= 1.01
    elif scroll_y < 0:
        scale *= 0.99


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camera_x, camera_y
    if buttons & mouse.LEFT:
        camera_x += dx
        camera_y += dy


pyglet.app.run()
