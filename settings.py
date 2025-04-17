import pygame as pg
from sys import exit as exit_process
vec2 = pg.math.Vector2
FPS = 60
TARGET_FPS = 60
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
TILE_SIZE = (SCREEN_WIDTH//29, SCREEN_WIDTH//29)
del screen
# TILE_SIZE = 64,64

BG_COLOR = (28, 29, 31)
