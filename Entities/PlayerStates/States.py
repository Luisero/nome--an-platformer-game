from ..State import State
from ..Animation import Animation
from settings import *

class IdleState(State):
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/idle.tmx', (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top),True,vec2(TILE_SIZE[0]*4, TILE_SIZE[1]),0.1)
        self.context.camera.add(self.animation)
    def input(self,input):
        if self.context.keys[pg.K_SPACE]:
            if self.context.is_grounded():
                self.animation.kill()
                return JumpState(self.context)
        
        if self.context.keys[pg.K_f]:
            current = pg.time.get_ticks()
            if current -  self.context.last_attack > self.context.attack_cooldown:
                self.animation.kill()
                return AttackingState(self.context)
       
        if self.context.velocity.y > 0:
            self.animation.kill()
            return FallingState(self.context)

        
        if input.x !=0:
            self.animation.kill()
            return RunningState(self.context) 
        
    def update(self,dt):
        self.animation.play(self.context.anim_flip)
        
        self.animation.rect.topleft = (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top)
    
    def __str__(self):
        return 'IDLE'


class FallingState(State) :
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/fall.tmx', (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top),False,vec2(TILE_SIZE[0]*4, TILE_SIZE[1]),0.2)
        self.context.camera.add(self.animation)

    
    def update(self,dt):
        self.animation.play(self.context.anim_flip)
        self.animation.rect.topleft = (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top)
        if self.context.collision_types['bottom']:
            self.animation.kill()
            return IdleState(self.context)
    
    def __str__(self):
        return 'FALLING'

class JumpState(State):
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/jump.tmx', (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top),False,vec2(TILE_SIZE[0]*4, TILE_SIZE[1]),0.2)
        self.context.camera.add(self.animation)

        self.jump_sound = pg.mixer.Sound('Assets/Sounds/zapsplat_cartoon_comic_ruler_twang_wood_short_006_108519.mp3')
        self.jump_sound.play()
        self.jump_sound.set_volume(0.5)

    def input(self,input):
        pass
                
    def update(self, dt):
        self.animation.play(self.context.anim_flip)
        self.animation.rect.topleft = (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top)
        if self.context.velocity.y > 0:
            self.animation.kill()
            self.jump_sound.stop()
            return FallingState(self.context)
        
        if self.context.collision_types['top']:
            self.animation.kill()
            self.jump_sound.stop()
            return FallingState(self.context)
    
    
    def __str__(self):
        return 'JUMPING'
            



class RunningState(State):
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/run.tmx', (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top),True,vec2(TILE_SIZE[0]*4, TILE_SIZE[1]),0.2)
        self.context.camera.add(self.animation)

    def input(self,key):
        pass 

    def update(self,dt):
        self.animation.play(self.context.anim_flip)
        self.animation.rect.topleft = (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top)

        if self.context.velocity.y < 0:
            self.animation.kill()
            return JumpState(self.context)
      
        if self.context.collision_types['left'] or self.context.collision_types['right'] or self.context.velocity.x == 0:
            self.animation.kill()
            return IdleState(self.context)
        
    def __str__(self):
        return 'RUNNING'
            

class AttackingState(State):
    def __init__(self, context):
        super().__init__(context)

        self.initial_time = pg.time.get_ticks()
        self.animation = Animation('Assets/Sprites/attack.tmx', (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top),False,vec2(TILE_SIZE[0]*4, TILE_SIZE[1]),0.5)
        self.context.camera.add(self.animation)

    def update(self, dt):
        current = pg.time.get_ticks()
        self.animation.play(self.context.anim_flip)
        self.animation.rect.topleft = (self.context.rect.left-TILE_SIZE[0]*2,self.context.rect.top)

        if current - self.initial_time > self.context.attack_duration:
            self.context.last_attack = pg.time.get_ticks()
            self.animation.kill()
            return IdleState(self.context)
        
    def __str__(self):
        return "Attacking"
        
    
