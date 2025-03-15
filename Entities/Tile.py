import pygame as pg
import random
import math
from settings import *
class Tile(pg.sprite.Sprite):
    def __init__(self,position:vec2, surface:pg.Surface, group, collide=True) -> None:
        super().__init__(group)
        self.image = surface
        #self.original_position = [position[0], position[1]]
        #self.position = [position[0], position[1]+200]
        self.position = position
        self.collide = collide
        
        
        self.rect = self.image.get_frect(topleft =self.position)
        

        
    def draw(self, surface:pg.Surface, scroll=vec2(0,0)):
        pos = self.rect.topleft - scroll
        

        if pos.x >-TILE_SIZE[0] and pos.x <= SCREEN_WIDTH and pos.y >= -TILE_SIZE[1] and pos.y <= SCREEN_HEIGHT:
            surface.blit(self.image,pos)
        
    
        
    def update_collider(self, collider):
        self.collider = collider
    def update(self):
        
        
        self.rect.topleft = self.position
