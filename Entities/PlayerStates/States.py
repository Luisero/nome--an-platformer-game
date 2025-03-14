from ..State import State
from settings import *

class IdleState(State):
    def __init__(self, context):
        super().__init__(context)

    def input(self,input):
        if self.context.keys[pg.K_SPACE]:
            if self.context.is_grounded():
                return JumpState(self.context)
        
       
        if self.context.velocity.y > 0:
            return FallingState(self.context)

        
        if input.x !=0:
            return RunningState(self.context) 
        
    
    
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
        
    
    
    def __str__(self):
        return 'JUMPING'
            



class RunningState(State):
    def __init__(self, context):
        super().__init__(context)

    def input(self,key):
        pass 

    def update(self,dt):
        if self.context.velocity.y < 0:
            return JumpState(self.context)
      
        if self.context.collision_types['left'] or self.context.collision_types['right'] or self.context.velocity.x == 0:
            return IdleState(self.context)
        
    def __str__(self):
        return 'RUNNING'
            