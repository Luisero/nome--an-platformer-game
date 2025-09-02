import pygame as pg
from settings import *
from Entities.Pickable import Pickable
from Entities.Animation import Animation


class Coin(Pickable):
    def __init__(self, pos: vec2, player, camera):
        super().__init__(pos)
        self.player = player
        self.camera = camera
        self.pos = pos
        
        self.animation = Animation('./Assets/Sprites/coin.tmx', self.pos, True)
        self.camera.add(self.animation)

    def update(self):

        self.animation.play()
        self.animation.rect.topleft = self.pos
        

    def on_collected(self):
        self.player.coins += 1
        self.animation.kill()
