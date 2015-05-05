#!/usr/bin/env python

import pyglet
from pyglet.image.codecs.pil import PILImageDecoder

tiles_image = pyglet.image.load('tiles.png', decoder=PILImageDecoder())
tiles = pyglet.image.ImageGrid(tiles_image, 16, 16)

level_image = pyglet.image.load('level.bmp', decoder=PILImageDecoder())
level_rawimage = level_image.get_image_data()
format = 'RGB'
pitch = level_rawimage.width * len(format)
level_rawimage_array = bytearray(level_rawimage.get_data(format, pitch))

lookup_table_tiles = {(0,255,0):0, (0,255,255):4, (127,127,127):1, (153,153,153):2, (0,0,0):3}

level_width = level_rawimage.width
level_height = level_rawimage.height
tile_width = 32
tile_height = 32

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

sprites = []
level = []
#for i in range(0, level_rawimage_array.len(), 3):
for i in range(0, level_width*level_height*3, 3):
    r = level_rawimage_array[i]
    g = level_rawimage_array[i+1]
    b = level_rawimage_array[i+2]
    level.append(tiles[lookup_table_tiles[(r, g, b)]])
    sprites.append(pyglet.sprite.Sprite(level[-1], batch=batch, group=background))

#sprites = [pyglet.sprite.Sprite(tiles[0], batch=batch, group=background) for _ in range(4*4)]

for index, sprite in enumerate(sprites):
    sprite.x = (index % level_width) * 32
    sprite.y = (index // level_height) * 32
    #print("x = {}; y = {}".format(sprite.x, sprite.y))

window = pyglet.window.Window(level_width*tile_width, level_height*tile_width)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()
