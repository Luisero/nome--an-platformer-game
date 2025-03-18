from settings import *
from random import randint
from Entities.Bullet import Bullet
class Enemy(pg.sprite.Sprite):
    def __init__(self, position: vec2, tilemap):
        super().__init__()
        self.image = pg.surface.Surface((TILE_SIZE[0]//2, TILE_SIZE[1]))
        self.image.fill('yellow')
        self.position = position
        self.rect = self.image.get_frect(topleft=position)

        self.scroll = vec2(0,0)

        self.move_speed = vec2(4, 4)
        self.gravity = 1.2
        self.acceleration = vec2(0, self.gravity)
        self.JUMP_FORCE = -20
        self.velocity = vec2(0, 0)

        self.life = 60

        self.input = vec2(0, 0)
        self.randomize_direction()

        self.collision_list = []
        self.tilemap = tilemap
        self.ground = False
        self.collision_types = {"left": False, "right": False, "bottom": False, "top": False}
        self.blockers = []

        self.bullets = pg.sprite.Group()
        self.player_pos =vec2(0,0)

        self.change_direction_time = pg.time.get_ticks()  # Track when to change direction
        self.change_interval = 2000  # Change direction every 2 seconds

        self.last_shot = pg.time.get_ticks()
        self.shoot_interval = 800

        self.can_shoot = True

    def randomize_direction(self):
        """Chooses a new random movement direction or stops moving."""
        self.input = vec2(randint(-1, 1), randint(-1, 1))
        while self.input.length() == 0:  # Avoid (0,0) unless explicitly allowed
            self.input = vec2(randint(-1, 1), randint(-1, 1))
        self.input = self.input.normalize()

    def change_input(self):
        """Reverses direction upon collision."""
        collisions = [blocker for blocker in self.blockers if blocker.colliderect(self.rect)]
        for rect in collisions:
            if self.velocity.x > 0:
                self.collision_types["right"] = True
                self.input.x *= -1
            elif self.velocity.x < 0:
                self.collision_types["left"] = True
                self.input.x *= -1
    def shoot(self):
        if self.can_shoot:
                
                distance  = self.position - vec2(self.player_pos.x, self.player_pos.y+ TILE_SIZE[1]/2)
                if distance.length() < 800:
                    bullet = Bullet(vec2(self.position), vec2(self.player_pos.x, self.player_pos.y+ TILE_SIZE[1]/2), True)
                    bullet.speed = 7

                    self.bullets.add(bullet)
                    self.can_shoot = False

    def get_player_pos(self, player_pos):
        self.player_pos = player_pos
    def load_blockers(self, blockers):
        self.blockers = blockers

    def is_grounded(self):
        return self.ground

    def manage_collision_x(self):
        for tile in self.collision_list:
            if self.velocity.x > 0:
                self.rect.right = tile.rect.left
                self.collision_types["right"] = True
            elif self.velocity.x < 0:
                self.rect.left = tile.rect.right
                self.collision_types["left"] = True

    def manage_collision_y(self):
        for tile in self.collision_list:
            if self.velocity.y > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types["bottom"] = True
                self.velocity.y = 0
                self.ground = True
            elif self.velocity.y < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types["top"] = True
                self.velocity.y = 0

    def update(self, dt):
        """Updates the enemy movement and collision detection."""
        
        self.ground = False
        current_time = pg.time.get_ticks()

        self.bullets.update(dt)
        if current_time - self.last_shot > self.shoot_interval:
            self.last_shot = current_time
            self.can_shoot = True
        
        self.shoot()

        # Change direction every X seconds
        if current_time - self.change_direction_time > self.change_interval:
            self.randomize_direction()
            self.change_direction_time = current_time
            if self.input.x == 0:
                self.change_interval = 1000
            else:
                self.change_interval = 2000
            

        self.change_input()
        self.velocity.x = self.input.x * self.move_speed.x
        self.velocity.y += self.acceleration.y * dt

        self.collision_types = {"left": False, "right": False, "bottom": False, "top": False}

        self.position += self.velocity * dt

        self.rect.x = self.position.x
        self.collision_list = self.tilemap.get_collision_with(self)
        self.manage_collision_x()

        self.rect.y = self.position.y
        self.collision_list = self.tilemap.get_collision_with(self)
        self.manage_collision_y()

        self.position = vec2(self.rect.topleft)

        if self.position.y > 4000:
            self.kill()

    def draw(self, surface: pg.Surface, scroll=vec2(0, 0)):
        self.scroll = scroll
        """Draws the enemy and its collision boxes for debugging."""
        #for rect in self.blockers:
        #    pg.draw.rect(surface, "red", (rect.x - scroll.x, rect.y - scroll.y, rect.width, rect.height), 2)

        surface.blit(self.image, self.rect.topleft - scroll)
