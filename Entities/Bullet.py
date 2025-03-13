from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, position:vec2, shot_to:vec2):
        super().__init__()
        self.position = position
        self.shot_to = shot_to
        self.image = pg.surface.Surface((10,10))
        self.image.fill('blue')
        self.rect = self.image.get_frect()
        self.rect.topleft = self.position
        self.speed = 10
        self.direction = vec2(self.shot_to.x-self.position.x, self.shot_to.y - self.position.y)
        if self.direction.length != 0:
            pass
            self.direction = self.direction.normalize()

        
    
    def update(self):
        self.position += self.direction * self.speed
        self.rect.topleft = self.position

        

    def draw(self, surface, scroll):
        
        
        pos = self.position - scroll
        if pos.x < 0 or pos.x > SCREEN_WIDTH or pos.y < 0 or pos.y  >  SCREEN_HEIGHT:
            self.kill()
        surface.blit(self.image, pos)