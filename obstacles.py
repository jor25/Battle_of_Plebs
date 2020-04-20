# Class for in game obstacles and potentially objects.
# Date: 4-17-20

import pygame
import random
from configs import *

class Obstacles:
    def __init__(self, category, coords, id):
        self.id = id
        self.category = category        # 0 is wall, 1 will be something else
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.pre_x, self.pre_y, self.pre_w, self.pre_h = coords         # Explosion coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.hold_time = 10
        self.held_for = self.hold_time           # Needs to be held for 10 frames before being able to drop

        self.boom_timer = 5         # Countdown from 5
        self.frames_before_dec = FPS    # How many frames go by before decrementing boom timer

        self.shock_wave = -self.boom_timer  # How far out it extends
        self.fbe = int(FPS/10)              # Frames before explode

        self.dead = False           # Once this is true, remove it.
        self.activated = False      # Activated when picked up
        self.exploding = False
        self.picked_up = False      # Only let it be picked up if this is false

    def blow_up(self):  # If category is 1, it can explode
        if self.category == 1:  # It can do this
            print("BOOM")

    def item_picked_up(self):       # The item was picked up
        if self.category == 1:      # Item
            self.picked_up = True   # Item is picked up
            self.activated = True   # Activate the item
            print("Item Activated".format())

    def item_put_down(self):    # Place the item down
        if self.category == 1:          # Item
            self.picked_up = False      # Item is placed down
            self.held_for += 1          # Increment held_time
            print("PLACED ITEM")

    def draw(self, window):
        if not self.dead:
            if self.category == 0:      # Walls
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

            elif self.category == 1:    # Items
                if self.activated:      # Activated - starts out not activated until it's picked up
                    color_num = random.randint(0, 255)      # Activate
                else:
                    color_num = 0       # Not active
                pygame.draw.rect(window, (0, 0, color_num), self.hitbox, 10)

            if self.held_for < self.hold_time and not self.picked_up:    # Increment only if not being held and less than 5
                self.held_for += 1  # Increment held_for every frame

            if self.activated and self.boom_timer > 0:
                if self.frames_before_dec > 0:
                    self.frames_before_dec -= 1 # Decrement counter
                else:
                    self.frames_before_dec = FPS    # reset
                    self.boom_timer -= 1
                text_obj = SIMP_FONT.render("{}".format(self.boom_timer), 1, (0, 255, 0))
                text_rect = text_obj.get_rect()
                text_rect.topleft = (int(self.x+ITEM_DIM/4), int(self.y+ITEM_DIM/4))  # Where to place the text
                window.blit(text_obj, text_rect)
            elif self.boom_timer == 0:  # BOOM
                self.exploding = True   # OK, it's exploding now
                print("BOOM")
                pygame.draw.rect(window, (255, 255, 0), (self.x - 20, self.y - 20, self.w + 40, self.h + 40), 10)
                self.boom_timer -= 1

            elif 0 > self.boom_timer > self.shock_wave: # Has it fully exploded
                if self.fbe> 0:
                    self.fbe -= 1 # Decrement counter
                else:
                    self.fbe = int(FPS/10)    # reset
                    self.boom_timer -= 1
                    print(self.boom_timer)

                pos_ratio = int(0/(-self.shock_wave))
                neg_ratio = int(255/(-self.shock_wave))

                self.x = self.pre_x - (20 * -self.boom_timer)
                self.y = self.pre_y - (20 * -self.boom_timer)
                self.w = self.pre_w + (40 * -self.boom_timer)
                self.h = self.pre_h + (40 * -self.boom_timer)

                pygame.draw.rect(window, (255+pos_ratio*-self.boom_timer, 255-neg_ratio*-self.boom_timer, 0),
                                 (self.x, self.y, self.w, self.h), 10)
                if self.boom_timer == self.shock_wave:
                    self.dead = True    # Explosion done
                    print("Explosion done")