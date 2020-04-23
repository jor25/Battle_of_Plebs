# Plebs file, where players are defined
# Date: 4-14-20

from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
from configs import *


# Initialize the plebs
class Plebs:
    def __init__(self, id, coords, my_sprites):
        '''
        Initialize the pleb to an initial location with a specific size and id value.
        :param id: pleb identification integer.
        :param coords: list of integers in the format of [x,y,w,h]
        '''
        self.id = id                                    # Player's ID number
        self.category = -1                              # Indicate this is a pleb
        self.init_coords = coords                       # Hold original position
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.vel = 10                                   # How fast the player moves
        self.left_or_right = 0                          # Left = 0, Right = 1

        # Creates a bunch of sprites
        self.sprites = self.make_my_sprites(my_sprites, '#00FF31', use_og=True)
        self.my_items = []          # The items I have
        self.alive = True           # While alive
        self.player = False         # Initially they aren't players

        print("This is pleb[{}]".format(id))    # DEBUG

    def reset_pleb(self):
        '''
        Resets the plebs back to where they initially started at the beginning of the game.
        Resets all initial parameters.
        :return: N/A
        '''

        self.x, self.y, self.w, self.h = self.init_coords       # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)          # Set up location

        self.left_or_right = 0      # Left = 0, Right = 1
        self.my_items = []          # The items I have
        self.alive = True           # While alive
        self.player = False         # Initially they aren't players


    def make_my_sprites(self, sprite_images, color_tint, use_og=False):
        '''
        Makes in game sprite objects for plebs.
        :param sprite_images: List of string paths to images to stitch together
        :param color_tint: String hexcode tint of color to modify the in game sprite '#00ff31'
        :param use_og: Boolean, tint or not to tint, use orignal image or tint it.
        :return: list of sprite image objects
        '''

        my_sprites = []                 # Initialize empty list of sprites
        for image in sprite_images:     # Loop through all paths
            if not use_og:              # Using color tint
                my_png = self.image_tint(image, color_tint)
                png_mode = my_png.mode
                png_size = my_png.size
                png_data = my_png.tobytes()
                my_sprites.append(pygame.image.fromstring(png_data, png_size,
                                                          png_mode).convert_alpha())  # Append the pygame sprite image
            else:       # Use original sprite
                my_sprites.append(pygame.image.load(image).convert_alpha())     # Append pygame sprite image

        return my_sprites       # Give back a list of sprite images

    def image_tint(self, source_path, tint='#ffffff'):
        '''
        Take an image from a path and convert it to a tinted string for sprite coloration.
        :param source_path: sting path to image
        :param tint: string color code in hex
        :return: string of modified image
        '''

        img_source = Image.open(source_path)                # Get the image from specified path
        tint_red, tint_green, tint_blue = getrgb(tint)      # Get color tint of each color
        tint_lum = getcolor(tint, "L")                      # Tint color luminosity

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
        '''
        Function to allow human to control the pleb with arrow keys and spacebar.
        :return: Player's move as an integer
        '''
        keys = pygame.key.get_pressed()     # Collect the key presses from user
        move = 0                            # Initialize a move to do nothing

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

        # Pick up/set down
        elif keys[pygame.K_SPACE]:
            move = 5

        return move     # Move from player

    def do_move(self, move):
        '''
        Take the move and perform the action with the pleb.
        Then updates the hitboxes of pleb and their items.
        :param move: integer from 0-4
        :return: N/A
        '''

        if move == 0:               # do nothing
            pass    # Do nothing

        elif move == 1:             # go left
            self.x -= self.vel
            self.left_or_right = 0  # Facing left now

        elif move == 2:             # go right
            self.x += self.vel
            self.left_or_right = 1  # Facing right now

        elif move == 3:             # go up
            self.y -= self.vel

        elif move == 4:             # go down
            self.y += self.vel

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)

        # Update hitbox of my item(s)
        for item in self.my_items:
            # Calculate coordinates for item placement
            x_item = (self.x + self.w) - item.w     # Get x coordinate in relation to pleb
            y_item = (self.y + self.h) - item.h     # Get y coordinate in relation to pleb
            item.x = x_item                         # Update x coord
            item.y = y_item                         # Update y coord
            item.pre_x = x_item                     # Update previous x coordinates
            item.pre_y = y_item                     # Update previous y coordinates
            item.hitbox = (x_item, y_item, item.w, item.h)      # Item hitbox updated

            if item.held_for > 0:
                item.held_for -= 1      # Subtract from timer until zero

            if item.exploding:      # If it's exploding, automatically DROP IT
                self.set_down()     # Drop the item

    def undo_move(self, move):
        '''
        Takes a move and undoes it. Then updates pleb hitbox.
        :param move: integer from 1-4
        :return: N/A
        '''
        if move == 1:               # undo go left
            self.x += self.vel

        elif move == 2:             # undo right
            self.x -= self.vel

        elif move == 3:             # undo go up
            self.y += self.vel

        elif move == 4:             # undo go down
            self.y -= self.vel

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)

    def pick_up(self, item):
        '''
        Allows pleb to pick up an item.
        :param item: Obstacle object
        :return: N/A
        '''
        # Pick up the item
        if not item.picked_up:          # If it hasn't been picked up, time to pick it up
            self.my_items.append(item)  # It's my item now
            item.item_picked_up()       # This item was picked up
            print(self.my_items)        # DEBUG
        else:
            print("Item already picked up")     # DEBUG

    def set_down(self):
        '''
        Pleb sets down whatever item it has. FIFO style.
        :return: N/A
        '''
        if len(self.my_items) > 0:                      # Have at least one item
            if self.my_items[0].held_for <= 0:          # Can only put down if it's zero or less
                self.my_items[0].item_put_down()        # Put down the first item
                print("item_location = {}".format(self.my_items[0].hitbox))     # DEBUG
                self.my_items.pop(0)                    # Remove the first item from my list
                print("pleb: {}\tItems: {}".format(self.id, self.my_items))     # DEBUG
            else:
                print("Hold longer")        # DEBUG
        else:
            print("No items to set down")   # DEBUG

    def check_collision(self, obsts):
        '''
        Check to see if the move I just made resulted in a collision with the given obstacle or pleb.
        :param obsts: Class object of pleb or obstacle class
        :return: Boolean collision and Integer index
        '''

        collision = False   # Haven't run into anything
        index = None        # No index to return

        for i, obst in enumerate(obsts):
            if self.y < obst.y + obst.h:        # Check my y coords with wall y coords
                if self.y + self.h > obst.y:    # Are we on a collision path?
                    # Within hitbox x coords
                    if self.x + self.w > obst.x:        # Check my x coords with wall
                        if self.x < obst.x + obst.w:    # Is the wall above or below me?

                            if obst.category == 0:      # Wall
                                print("CONTACT [{}] with wall".format(self.id))     # DEBUG
                                collision = True    # Did I collide with wall?
                                index = i           # Give back this wall index

                            elif obst.category == 1:  # Item
                                if not obst.dead:       # Item is still on screen
                                    # Only collide with item if it hasn't been picked up and hasn't exploded
                                    if not obst.picked_up and not obst.exploding:
                                        # It's been placed for at least 5 frames
                                        if obst.held_for >= obst.hold_time:
                                            print("CONTACT [{}] with item[{}]".format(self.id, obst.id))    # DEBUG
                                            collision = True    # Did I collide with item?
                                            index = i           # Give back the item index

                                    elif obst.exploding:    # If object is exploding, check if in range of explosion
                                        print("CONTACT [{}] with explosion[{}]".format(self.id, obst.id))   # DEBUG
                                        collision = True    # Did I collide with explosion hitbox?
                                        index = i           # Give back the index
                                        self.alive = False  # Pleb is dead
                                        print("Pleb[{}] is dead".format(self.id))   # DEBUG

                            elif obst.category == -1:       # Fellow pleb
                                if obst.id != self.id:      # This is not me
                                    print("CONTACT [{}] with pleb!".format(self.id))    # DEBUG
                                    collision = True    # Did I collide with another pleb?
                                    index = i           # Give back pleb index

        return collision, index     # Let me know if I collided with something and the index of that something

    def draw(self, window, frames):
        '''
        Draw the sprites to the game window.
        :param window:
        :param frames:
        :return:
        '''

        # Draw only still living sprites
        if self.alive:
            if self.left_or_right == 1:     # If pleb is facing right
                # Display pleb sprite facing to the right - scale image to the right size as well
                window.blit(pygame.transform.flip(
                    (pygame.transform.scale(self.sprites[frames % len(self.sprites)], (self.w, self.h))),
                    True, False), (self.x, self.y))

            else:
                # Display pleb facing to the left - scale them to the right size as well
                window.blit(pygame.transform.scale(self.sprites[frames % len(self.sprites)],
                                                   (self.w, self.h)), (self.x, self.y))

            # DEBUG
            if self.player:
                pygame.draw.rect(window, (0, 255, 0), self.hitbox, 2)  # Draw hit box
            else:
                pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)  # Draw hit box

        for item in self.my_items:      # Draw all the items this pleb has if it has any
            item.draw(window)           # Draw the items