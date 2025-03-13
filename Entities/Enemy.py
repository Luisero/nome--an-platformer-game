from settings import *
from random import randint
class Enemy(pg.sprite.Sprite):
    def __init__(self,position:vec2, tilemap):
        super().__init__()
        self.image = pg.surface.Surface((32,64))
        self.image.fill('yellow')
        self.position = position
        self.rect = self.image.get_frect(topleft=position)


        self.move_speed = vec2(7,7)
        self.input = vec2(0,0)
        self.gravity = 1.2
        self.acceleration = vec2(0,self.gravity)
        self.JUMP_FORCE = -20
        self.velocity = vec2(0,0)

        self.input = vec2(randint(-1,1),randint(-1,1))
        if self.input.length() != 0:
            self.input = self.input.normalize()

        self.collision_list = []
        self.tilemap = tilemap
        self.ground = False
        self.collision_types = {"left": False, "right":False, "bottom": False, "top": False}
        
    def change_input(self):
        pass

    def is_grounded(self):
        if self.ground:
            return True 
        return False
    def check_jump(self):
        keys = pg.key.get_pressed()
        '''if keys[pg.K_SPACE] and self.is_grounded():
            self.velocity.y = self.JUMP_FORCE
        else: 
            self.acceleration.y =self.gravity'''

    def manage_collision_x(self):

        for tile in self.collision_list:
            if self.velocity.x > 0:
                self.rect.right = tile.rect.left
                self.collision_types["right"] = True 
                
                
            elif self.velocity.x < 0 :
                self.rect.left = tile.rect.right
                self.collision_types['left'] = True
                
                
                            

    def manage_collision_y(self):
        for tile in self.collision_list:
            if self.velocity.y > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types["bottom"] = True 
                
                self.velocity.y = 0
                self.ground = True
            elif self.velocity.y < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types['top'] = True
                self.velocity.y = 0

    def update(self,dt):
        self.check_jump()
        #self.acceleration.y *=dt
        self.ground = False

        input = self.change_input()
        #self.velocity = vec2(0,0)
        self.velocity.x = self.input.x * self.move_speed.x
        #self.velocity.y = input.y * self.move_speed.y
        self.velocity.y += self.acceleration.y * dt
        

        self.collision_types = {"left": False, "right":False, "bottom": False, "top": False}

        self.position += self.velocity * dt 
        
        self.rect.x = self.position.x
        self.collision_list = self.tilemap.get_collision_with(self)

        self.manage_collision_x()
        self.rect.y = self.position.y
        self.collision_list = self.tilemap.get_collision_with(self)
        self.manage_collision_y()
        
        

        #self.rect.topleft = self.position
        self.position = vec2(self.rect.topleft)
        
        if self.position.y > 4000:
            self.kill()


    def draw(self, surface:pg.Surface, scroll=vec2(0,0)):
            surface.blit(self.image,self.rect.topleft-scroll)
            
            