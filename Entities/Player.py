from settings import *
from Entities.Animation import Animation
from Entities.Bullet import Bullet
from Entities.Arm import Arm
from .PlayerStates.States import *
class Player(pg.sprite.Sprite):
    def __init__(self,position:vec2, tilemap, camera):
        super().__init__()
        self.image = pg.surface.Surface((TILE_SIZE[0]//2,TILE_SIZE[1]))
        self.image.fill('red')
        self.position = position
        self.rect = self.image.get_frect(topleft=position)

        self.camera = camera

        self.arm = Arm(vec2(self.rect.topright),0)
        self.move_speed = vec2(5,5)
        self.input = vec2(0,0)
        self.gravity = 1.2
        self.acceleration = vec2(0,self.gravity)
        self.JUMP_FORCE = -23
        self.velocity = vec2(0,0)
        self.keys = pg.key.get_pressed()

        self.bullets = pg.sprite.Group()
        self.scroll = vec2(0,0)

        self.life = 100
        
        self.mouse_pos = self.get_mouse_pos()
        self.collision_list = []
        self.tilemap = tilemap
        self.ground = False
        self.collision_types = {"left": False, "right":False, "bottom": False, "top": False}

        self.active_state = IdleState(self)
    

        self.anim_flip = False

        self.can_shoot = True   
        self.current_time = pg.time.get_ticks()
        self.shoot_interval = 700

        self.attack_duration = 400

        self.attack_cooldown = 1000
        self.last_attack = 0

        self.dash_points = 0

        self.ammo = 64

    
    def get_mouse_pos(self):
        x,y = pg.mouse.get_pos()
        return vec2(x,y)

    def get_input(self):
        input = vec2()
        
        if self.keys[pg.K_a]:
            input.x -=1
        if self.keys[pg.K_d]:
            input.x +=1
        if self.keys[pg.K_w]:
            input.y -=1
        if self.keys[pg.K_s]:
            input.y +=1
        
        if input.length() != 0:
            input = input.normalize()
    
        return input

    def is_grounded(self):
        if self.ground:
            return True 
        return False
    def check_jump(self):
        
        if self.keys[pg.K_SPACE] and self.is_grounded():
            self.velocity.y = self.JUMP_FORCE 
        else: 
            self.acceleration.y =self.gravity

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
    
    def update_keys(self):
        self.keys = pg.key.get_pressed()


    def shoot(self):
        if self.can_shoot:
            if (self.keys[pg.K_k] or pg.mouse.get_pressed()[0]) and self.ammo > 0 :
                bullet = Bullet(vec2(self.arm.rect.midright), self.mouse_pos+ self.scroll)

                self.bullets.add(bullet)
                self.can_shoot = False
                self.ammo -=1
    def handle_collison(self):
        self.collision_types = {"left": False, "right":False, "bottom": False, "top": False}

        self.position += self.velocity * self.dt 
        
        self.rect.x = self.position.x
        self.collision_list = self.tilemap.get_collision_with(self)

        self.manage_collision_x()
        self.rect.y = self.position.y
        self.collision_list = self.tilemap.get_collision_with(self)
        self.manage_collision_y()
        pass
    def update(self,dt):
        input = self.get_input()
        self.dt = dt
        new_state = self.active_state.input(input)
        
        if new_state:
            del self.active_state
            self.active_state = new_state

        new_state = self.active_state.update(self.dt)
        aim_pos = self.get_mouse_pos() + self.scroll
        self.arm.update(vec2(self.rect.center),aim_pos)
        
        if new_state:
            del self.active_state
            self.active_state = new_state

        self.check_jump()
        #self.acceleration.y *=dt
        self.ground = False
        self.update_keys()
        self.mouse_pos = self.get_mouse_pos()



        current_time = pg.time.get_ticks()
        if current_time - self.current_time >= self.shoot_interval:
            self.current_time= pg.time.get_ticks()
            self.can_shoot = True

        self.shoot()
        self.bullets.update(dt)

        #self.velocity = vec2(0,0)
        self.velocity.x = input.x * self.move_speed.x
        #self.velocity.y = input.y * self.move_speed.y
        self.velocity.y += self.acceleration.y * dt
        self.velocity.x += self.acceleration.x *dt
        
        if self.velocity.x < 0:
            self.anim_flip = True 
        elif self.velocity.x == 0 and self.anim_flip == True:
            self.anim_flip = True 
        elif self.velocity.x >0:
            self.anim_flip = False

       
        
        self.handle_collison( )

        #self.rect.topleft = self.position
        self.position = vec2(self.rect.topleft)
        
        


    def draw(self, surface:pg.Surface, scroll=vec2(0,0)):
            self.scroll = scroll
           # surface.blit(self.image,self.rect.topleft-scroll)
            self.arm.draw(surface, scroll)

            font = pg.font.Font(None, 36)
            state_text = font.render(f"State: {self.active_state}", True, (255, 255, 255))
            surface.blit(state_text, (10, 130))
            ammo_text = font.render(f'Ammo: {self.ammo}', True, (255,255,255))
            surface.blit(ammo_text, (10, 170))
                