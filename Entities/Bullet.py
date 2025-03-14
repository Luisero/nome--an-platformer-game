from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, position:vec2, shot_to:vec2, enemy_bullet=False):
        super().__init__()
        self.position = position
        self.shot_to = shot_to
        self.image = pg.surface.Surface((10,10)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_frect()
        self.rect.topleft = self.position
        self.speed = 10
        self.direction = vec2(self.shot_to.x-self.position.x, self.shot_to.y - self.position.y)
        vec = vec2(1,0)
        self.angle = self.direction.angle_to(vec)
        self.image= pg.transform.rotate(self.image, self.angle)
        if self.direction.length != 0:
            self.direction = self.direction.normalize()

        self.enemy_bullet = enemy_bullet

        self.damage= 5

        self.time = 0
    
    def update(self,dt):
        #self.time +=1
        #self.image = pg.surface.Surface((10,10)).convert_alpha()
        
        #self.image.fill((0,0,255,max(0,min(255/(self.time/10),255))))
        self.position += self.direction * self.speed *dt
        self.rect.topleft = self.position


    

    def draw(self, surface, scroll):
        tolerance = 500
        
        pos = self.position - scroll
        if pos.x < -tolerance or pos.x > SCREEN_WIDTH+tolerance  or pos.y < -tolerance or pos.y  >  SCREEN_HEIGHT+tolerance:

            self.kill()
        surface.blit(self.image, pos)