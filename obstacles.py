# Class for in game obstacles and potentially objects.
# Date: 4-17-20

import random
from configs import *


# Class for in game objects such as walls and items.
class Obstacles:
    def __init__(self, category, coords, id):
        self.id = id                                                    # Object id
        self.category = category                                        # 0 is wall, 1 is item
        self.init_coords = coords                                       # Initial coords for reset
        self.x, self.y, self.w, self.h = coords                         # Initalize coords
        self.pre_x, self.pre_y, self.pre_w, self.pre_h = coords         # Explosion coords
        self.hitbox = (self.x, self.y, self.w, self.h)                  # Set up location
        self.hold_time = 10                                             # How long to hold an item
        self.held_for = self.hold_time                                  # Needs to be held for 10 frames before a drop

        self.boom_timer = 5                 # Countdown from 5
        self.frames_before_dec = 60         # How many frames go by before decrementing boom timer

        self.shock_wave = -self.boom_timer      # How far out explosion extends
        self.fbe = 5                            # Frames before explode

        self.dead = False           # Once this is true, remove it.
        self.activated = False      # Activated when picked up
        self.exploding = False      # Flag for Explosion
        self.picked_up = False      # Only let it be picked up if this is false

    def reset_obst(self):
        '''
        Resets all the item parameters and flags to their initial starting values.
        :return: N/A
        '''

        self.x, self.y, self.w, self.h = self.init_coords                       # Initalize coords
        self.pre_x, self.pre_y, self.pre_w, self.pre_h = self.init_coords       # Explosion coords
        self.hitbox = (self.x, self.y, self.w, self.h)                          # Set up location

        self.hold_time = 10                 # How long to hold an item
        self.boom_timer = 5                 # Countdown from 5
        self.frames_before_dec = 60         # How many frames go by before decrementing boom timer

        self.shock_wave = -self.boom_timer      # How far out explosion extends
        self.fbe = 5                            # Frames before explode

        self.dead = False           # Once this is true, remove it.
        self.activated = False      # Activated when picked up
        self.exploding = False      # Flag for Explosion
        self.picked_up = False      # Only let it be picked up if this is false

    def blow_up(self):          # If category is 1, it can explode CURRENTLY NOT USED
        if self.category == 1:  # It's an item and it can explode
            print("BOOM")       # DEBUG

    def item_picked_up(self):       # The item was picked up
        '''
        Let the item know that it has been picked up and it's coordinates are now controlled by the pleb.
        Also activates the item and starts the countdown.
        :return: N/A
        '''
        if self.category == 1:      # Item
            self.picked_up = True   # Item is picked up
            self.activated = True   # Activate the item
            print("Item Activated".format())    # DEBUG

    def item_put_down(self):    # Place the item down
        '''
        Let the item know it has been placed down and it's coordinates are its own again.
        Start incrementing the held_for time.
        :return: N/A
        '''
        if self.category == 1:          # Item
            self.picked_up = False      # Item is placed down
            self.held_for += 1          # Increment held_for time
            print("PLACED ITEM")    # DEBUG

    def draw(self, window):
        '''
        Draw the individual item or walls if they aren't dead.
        :param window:
        :return:
        '''

        # Display if the item is not dead
        if not self.dead:
            if self.category == 0:      # Display for walls
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)       # Red rectangles to block off the area

            elif self.category == 1:                        # Display for items
                if self.activated:                          # Activated - starts out not activated until it's picked up
                    color_num = random.randint(0, 255)      # Activate color ratio - starts making box flash
                else:
                    color_num = 0                           # Not active - dull no color change

                # Display the item as a black or flashing box
                pygame.draw.rect(window, (0, 0, color_num), self.hitbox, 10)

            # Increment only if item has not been held long enough and it's not picked up
            if self.held_for < self.hold_time and not self.picked_up:
                self.held_for += 1                  # Increment held_for every frame

            # Item has been activated and it's boom timer is greater than zero
            if self.activated and self.boom_timer > 0:
                if self.frames_before_dec > 0:      # If frames before decrement greater than zero
                    self.frames_before_dec -= 1     # Decrement counter
                else:
                    self.frames_before_dec = 60     # If it's zero or less, then reset frames before dec
                    self.boom_timer -= 1            # Boom timer decrements 1

                # Render countdown on the item
                text_obj = SIMP_FONT.render("{}".format(self.boom_timer), 1, (0, 255, 0))
                text_rect = text_obj.get_rect()
                text_rect.topleft = (int(self.x+ITEM_DIM/4), int(self.y+ITEM_DIM/4))        # Where to place the text
                window.blit(text_obj, text_rect)                                            # Blit the text

            # Countdown reached zero = BOOM
            elif self.boom_timer == 0:
                self.exploding = True   # OK, it's exploding now
                print("BOOM")           # DEBUG
                # Render the image
                pygame.draw.rect(window, (255, 255, 0), (self.x - 20, self.y - 20, self.w + 40, self.h + 40), 10)
                self.boom_timer -= 1    # Decrement boom timer

            # Has the item fully exploded
            elif 0 > self.boom_timer > self.shock_wave:
                if self.fbe > 0:    # Frames before explosion greater than zero
                    self.fbe -= 1   # Decrement counter
                else:
                    self.fbe = 5           # Reset frames before explosion
                    self.boom_timer -= 1    # Drop boom_timer lower
                    print(self.boom_timer)  # DEBUG

                # Determine color ratios for positive and negative increments
                pos_ratio = int(0/(-self.shock_wave))
                neg_ratio = int(255/(-self.shock_wave))

                # Expand the hitbox of the item to the size of the explosion
                self.x = self.pre_x - (20 * -self.boom_timer)
                self.y = self.pre_y - (20 * -self.boom_timer)
                self.w = self.pre_w + (40 * -self.boom_timer)
                self.h = self.pre_h + (40 * -self.boom_timer)

                # Render the explosion graphics to the screen
                pygame.draw.rect(window, (255+pos_ratio*-self.boom_timer, 255-neg_ratio*-self.boom_timer, 0),
                                 (self.x, self.y, self.w, self.h), 10)

                # The conclusion of the item's explosion
                if self.boom_timer == self.shock_wave:
                    self.dead = True            # Explosion done
                    print("Explosion done")     # DEBUG
