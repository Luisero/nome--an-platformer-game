from settings import *
from .Animation import Animation
from Entities.Explosion import Explosion
class Capacitor(pg.sprite.Sprite):
    def __init__(self,pos:vec2, camera ,player):
        super().__init__()

        self.pos = pos
        self.animation = Animation('Assets/Sprites/capacitor.tmx',pos,True, speed=0.05)
        self.camera = camera
        self.initial_explosion_time=0
        self.has_started=False 
        self.explosion_time = 1000
        self.player =player
        

        camera.add(self.animation)
        
    def update(self, explosion_group):
        vec_capacitor_player = vec2(self.pos - self.player.position)
        
        if vec_capacitor_player.length() < TILE_SIZE[0]*3:
            if not self.has_started:
                self.has_started = True 
                self.initial_explosion_time= pg.time.get_ticks()
            
        if self.has_started:
            current = pg.time.get_ticks()
            if current - self.initial_explosion_time >  self.explosion_time:
                explosion_group.add(Explosion(vec2(self.animation.rect.center),self.camera,self.player,1))
                self.animation.kill()
                self.kill()

        self.animation.play()
        self.animation.rect.topleft = self.pos
        
        

    
