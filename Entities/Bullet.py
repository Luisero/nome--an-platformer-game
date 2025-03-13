from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, position:vec2, shot_to:vec2):
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
            pass
            self.direction = self.direction.normalize()

        self.time = 0
    
    def update(self):
        self.time +=1
        self.image = pg.surface.Surface((10,10)).convert_alpha()
        
        self.image.fill((0,0,255,max(0,min(255/(self.time/10),255))))
        self.position += self.direction * self.speed
        self.rect.topleft = self.position


        

    def draw(self, surface, scroll):
        
        
        pos = self.position - scroll
        if pos.x < 0 or pos.x > SCREEN_WIDTH or pos.y < 0 or pos.y  >  SCREEN_HEIGHT:
            self.kill()
        surface.blit(self.image, pos)