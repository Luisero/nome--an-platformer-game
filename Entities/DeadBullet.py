from settings import *


class DeadBullet(pg.sprite.Sprite):
    def __init__(self, position:vec2, direction:vec2):
        super().__init__()
        self.position = position
        self.image = pg.surface.Surface((10,10)).convert_alpha()
        self.image.fill('cyan')
        self.rect = self.image.get_frect()
        self.rect.topleft = self.position
        self.speed = 2
        self.direction = direction
        vec = vec2(1,0)
        self.angle = self.direction.angle_to(vec)
        self.image= pg.transform.rotate(self.image, self.angle)
        if self.direction.length != 0:
            self.direction = self.direction.normalize()

  
        self.velocity = vec2(self.speed,0)
        self.acceleration = vec2(0,-0.01)
        self.time = 0
    
    def update(self,dt):
        self.time +=1
        
        self.image = pg.transform.scale(self.image, ((self.time+1)/2,(self.time)/2))
        self.image.fill((self.time,self.time,255,max(0,min(255/(self.time/10),255))))
        self.velocity += self.acceleration
        
        self.position += self.direction * self.velocity * vec2(dt,dt)
        self.rect.topleft = self.position
        if self.time* dt > 60:
            self.kill()
        #if self.image.get_alpha() < 10:
        #    self.kill()


    

    def draw(self, surface, scroll):
        tolerance = 500
        
        pos = self.position - scroll
        if pos.x < -tolerance or pos.x > SCREEN_WIDTH+tolerance  or pos.y < -tolerance or pos.y  >  SCREEN_HEIGHT+tolerance:

            self.kill()
        surface.blit(self.image, pos)