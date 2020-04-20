# Hold the game settings and configurations
# Also hold the game sprites
import pygame

pygame.init()  # Initialize the pygame instance

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
WALL_WIDTH = 25
ITEM_DIM = 40
FPS = 60

SIMP_FONT = pygame.font.SysFont(None, 40)  # Initialize a font  # Obstacle countdown timer

TITLE = 'images/BoP_Title.png'
# SPRITE Lists
ALL_SPRITES = [
                ['images/option_0_sprites/option_0_0.png',
                 'images/option_0_sprites/option_0_1.png',
                 'images/option_0_sprites/option_0_2.png'],

                ['images/option_1_sprites/option_1_0.png',
                 'images/option_1_sprites/option_1_1.png',
                 'images/option_1_sprites/option_1_2.png'],

                ['images/option_2_sprites/option_2_0.png',
                 'images/option_2_sprites/option_2_1.png',
                 'images/option_2_sprites/option_2_2.png'],

                ['images/option_3_sprites/option_3_0.png',
                 'images/option_3_sprites/option_3_1.png',
                 'images/option_3_sprites/option_3_2.png'],

                ['images/option_4_sprites/option_4_0.png',
                 'images/option_4_sprites/option_4_1.png',
                 'images/option_4_sprites/option_4_2.png'],

                ['images/option_5_sprites/option_5_0.png',
                 'images/option_5_sprites/option_5_1.png',
                 'images/option_5_sprites/option_5_2.png']
                ]