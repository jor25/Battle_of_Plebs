# Plebs file, where players are defined
# Date: 4-14-20

import pygame
import numpy as np
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale


class Plebs:                # Initialize the plebs
    def __init__(self, id, coords):
        '''
        Initialize the pleb to an initial location with a specific size and id value.
        :param id: pleb identification integer.
        :param coords: list of integers in the format of [x,y,w,h]
        '''
        self.id = id        # Player's ID number
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.vel = 10                                   # How fast the player moves
        self.sprites = self.make_my_sprites(['images/option_0.png', 'images/option_1.png'], '#00FF31')
        print("This is pleb[{}]".format(id))

    def make_my_sprites(self, sprite_images, color_tint):

        my_sprites = []
        for image in sprite_images:
            my_png = self.image_tint(image, color_tint)
            png_mode = my_png.mode
            png_size = my_png.size
            png_data = my_png.tobytes()
            my_sprites.append(pygame.image.fromstring(png_data, png_size,
                                                      png_mode).convert_alpha())  # Convert alpha makes it run faster?
        return my_sprites

    def image_tint(self, source_path, tint='#ffffff'):
        '''
        Take an image from a path and convert it to a tinted string for sprite coloration.
        :param source_path: sting path to image
        :param tint: string color code in hex
        :return: string of modified image
        '''
        img_source = Image.open(source_path)

        tint_red, tint_green, tint_blue = getrgb(tint)      # Get color tint of each color
        tint_lum = getcolor(tint, "L")  # Tint color luminosity

        if tint_lum == 0:   # Avoid division by 0
            tint_lum = 1

        tint_lum = float(tint_lum)  # Compute luminosity preserving tint factors
        sr, sg, sb = map(lambda tv: tv / tint_lum, (tint_red, tint_green, tint_blue))  # per component adjustments

        # create look-up tables to map luminosity to adjusted tint
        # (using floating-point math only to compute table)
        luts = (list(map(lambda lr: int(lr * sr + 0.5), range(256))) +
                list(map(lambda lg: int(lg * sg + 0.5), range(256))) +
                list(map(lambda lb: int(lb * sb + 0.5), range(256))))

        l = grayscale(img_source)  # 8-bit luminosity version of whole image

        if Image.getmodebands(img_source.mode) < 4:
            merge_args = (img_source.mode, (l, l, l))  # for RGB verion of grayscale
        else:  # include copy of img_source image's alpha layer
            a = Image.new("L", img_source.size)
            a.putdata(img_source.getdata(3))
            merge_args = (img_source.mode, (l, l, l, a))  # for RGBA verion of grayscale
            luts += range(256)  # for 1:1 mapping of copied alpha values

        return Image.merge(*merge_args).point(luts)     # Return string of image

    def active_player(self):
        keys = pygame.key.get_pressed()     # Collect the key presses from user
        move = 0                            # Initialize a move to go straight

        # Go left
        if keys[pygame.K_LEFT]:
            move = 1

        # Go Right
        elif keys[pygame.K_RIGHT]:
            move = 2

        # Go Up
        elif keys[pygame.K_UP]:
            move = 3

        # Go Down
        elif keys[pygame.K_DOWN]:
            move = 4

        return move     # Move from player

    def do_move(self, move):

        if move == 0:               # do nothing
            pass    # Do nothing

        elif move == 1:             # go left
            self.x -= self.vel

        elif move == 2:             # go right
            self.x += self.vel

        elif move == 3:             # go up
            self.y -= self.vel

        elif move == 4:             # go down
            self.y += self.vel

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)


    def draw(self, window, frames):
        #window.blit(self.sprites[0], (self.x, self.y))

        window.blit(pygame.transform.flip(
            (pygame.transform.scale(self.sprites[frames % len(self.sprites)], (self.w, self.h))),
            True, False), (self.x, self.y))