from ..State import State
from ..Animation import Animation
from settings import *

class IdleState(State):
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/idle.tmx', self.context.rect.topleft,True,vec2(self.context.image.get_size()),0.1)
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
        self.animation.rect.topleft = self.context.rect.topleft
    
    def __str__(self):
        return 'IDLE'


class FallingState(State) :
    def __init__(self, context):
        super().__init__(context)

    
    def update(self,dt):
        if self.context.collision_types['bottom']:
            return IdleState(self.context)
    
    def __str__(self):
        return 'FALLING'

class JumpState(State):
    def __init__(self, context):
        super().__init__(context)

    def input(self,input):
        pass
                
    def update(self, dt):
        if self.context.velocity.y > 0:
            return FallingState(self.context)
        
        if self.context.collision_types['top']:
            return FallingState(self.context)
    
    
    def __str__(self):
        return 'JUMPING'
            



class RunningState(State):
    def __init__(self, context):
        super().__init__(context)
        self.animation = Animation('Assets/Sprites/run.tmx', self.context.rect.topleft,True,vec2(self.context.image.get_size()),0.3)
        self.context.camera.add(self.animation)

    def input(self,key):
        pass 

    def update(self,dt):
        self.animation.play(self.context.anim_flip)
        self.animation.rect.topleft = self.context.rect.topleft

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

    def update(self, dt):
        current = pg.time.get_ticks()

        if current - self.initial_time > self.context.attack_duration:
            self.context.last_attack = pg.time.get_ticks()
            return IdleState(self.context)
        
    def __str__(self):
        return "Attacking"
        
    
