from settings import *
import math

class Arm(pg.sprite.Sprite):
    def __init__(self, pos: vec2, angle: float):
        super().__init__()

        self.pos = pos
        self.image = pg.image.load('Assets/Sprites/weapon.png').convert_alpha()
        self.image = pg.transform.scale(self.image,(self.image.get_width()*1.5,self.image.get_height()*1.5))
        self.rect = self.image.get_rect(center=pos)
        self.default_img = self.image.copy()
        self.angle = angle

    def update(self, pivot, aim_pos):
        aim_vec: vec2 = aim_pos - (pivot-vec2(self.rect.width/2,self.rect.height/2))
        angle = -math.degrees(math.atan2(aim_vec.y, aim_vec.x))
            
        # Rotaciona a imagem ao redor do pivot
        self.image = pg.transform.rotate(self.default_img, angle)
        
        
        #pivot.y +=20
        self.rect = self.image.get_rect(midleft=pivot)

    def draw(self, surface, scroll):
        pos = vec2(self.rect.topleft) - scroll
        surface.blit(self.image, pos)
