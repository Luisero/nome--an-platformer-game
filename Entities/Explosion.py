from settings import *
import math

class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def collide_with(self, pos):
        if pos.x > self.pos.x - self.radius and pos.x < self.pos.x + self.radius and pos.y > self.pos.y - self.radius and pos.y < self.pos.y + self.radius:
            return True 
        return False


class Explosion(pg.sprite.Sprite):
    def __init__(self, pos, camera, player, speed=0.1):
        super().__init__()

        self.pos = pos
        self.initial_pos = pos
        self.images =[]
        self.current_frame=0
        self.damage = 50

        self.speed= speed
        self.player = player
        camera.add(self)
        self.load_images()
        circle_pos = self.pos- vec2(TILE_SIZE)/4
        self.circle_collider = Circle(circle_pos, TILE_SIZE[0]*3)
        self.pos.x -= self.images[0].get_width()/2
        self.pos.y -= self.images[0].get_height()/2

        self.has_hit_player = False

    def load_images(self):
        for i in range(74):
            image = pg.image.load(f'Assets/Sprites/Explosion/frame00{i:02d}.png').convert_alpha()
            image = pg.transform.scale2x(image)
            image = pg.transform.scale2x(image)
            self.images.append(image)

    def check_collision_in_player(self):
        if self.circle_collider.collide_with(self.player.position):
         
            if not self.has_hit_player:
                self.player.life -= self.damage
                self.has_hit_player  = True
                vector_move = vec2()
                self.player.velocity.y += -35
                self.player.gravity = 1.1
                
                    

    def update(self):
        self.current_frame+=self.speed
        self.check_collision_in_player()

        if self.current_frame > len(self.images)-1:
            self.player.gravity = 1.2
            self.kill()

    def draw(self, surface,scroll):
        pos = self.pos - scroll
        #pg.draw.circle(surface,'red',self.circle_collider.pos-scroll,self.circle_collider.radius)

        surface.blit(self.images[int(self.current_frame)],pos)