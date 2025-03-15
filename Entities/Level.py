from settings import *
import time
import pytmx
from Entities.Camera import Camera
from Entities.Player import Player
from Entities.Tilemap import Tilemap


class Level:
    def __init__(self, number):
        self.number = number
        self.camera = Camera()
        self.tilemap = Tilemap(f'./Data/Levels/{self.number}.tmx')
        self.camera.add(self.tilemap.sprites())
        self.entities_group = pg.sprite.Group()
        self.tilemap.load_tiles()

        print('timse')

        self.rect_next_level_trigger =pg.Rect()
        self.dt = 0

        self.should_change_level=False

        self.player = self.tilemap.add_player(self.camera)
        self.player_group = pg.sprite.GroupSingle(self.player)
        self.initial_player_pos = self.player.position
        self.enemies = pg.sprite.Group()
        self.tilemap.add_enemies(self.camera, self.enemies)

        self.enemy_blockers = []
        self.add_enemy_blockers()
        for enemy in self.enemies.sprites():
            enemy.load_blockers(self.enemy_blockers)
        self.camera.add(self.player)
        self.entities_group.add(self.player)

        self.add_next_level_trigger()

    
    
        
    def update(self, dt):
        self.dt = dt
        self.tilemap.update()
        self.enemies.update(self.dt)
        self.entities_group.update(self.dt)
        self.camera.add(self.player.bullets)
        self.check_player_hit_enemy()
        self.check_enemy_hit_player()

        self.camera.update_scroll(self.player.rect)
        for enemy in self.enemies:
            enemy.get_player_pos(self.player.position)
            self.camera.add(enemy.bullets)

        if self.player.rect.colliderect(self.rect_next_level_trigger):
            self.should_change_level=True
            

        if self.player.position.y > 6000:
            self.player.position = self.initial_player_pos

    def check_player_hit_enemy(self):
        for bullet in self.player.bullets:
            hits = pg.sprite.spritecollide(bullet,self.enemies,False)
            for enemy in hits:
                enemy.life -= bullet.damage
                enemy.image.fill('orange')
                if enemy.life < 0:
                    enemy.kill()
                    for e_bullets in enemy.bullets:
                        e_bullets.kill()

    def check_enemy_hit_player(self):
        
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                hits = pg.sprite.spritecollide(bullet,self.player_group,False)
                for player in hits:
                    self.player.life -= bullet.damage
                    bullet.kill()

    
    def add_enemy_blockers(self):
        data = pytmx.load_pygame(f'./Data/Levels/{self.number}.tmx', pixelalpha=True)
        
        for obj in data.get_layer_by_name('Enemy blockers'):
            blocker_x = obj.x / data.tilewidth
            blocker_y = obj.y / data.tileheight
                
            rect = pg.Rect(blocker_x* TILE_SIZE[0],blocker_y*TILE_SIZE[1], TILE_SIZE[0],TILE_SIZE[1])
            
            self.enemy_blockers.append(rect)

    def add_next_level_trigger(self):
        data = pytmx.load_pygame(f'./Data/Levels/{self.number}.tmx', pixelalpha=True)

        for obj in data.get_layer_by_name('Next'):
            blocker_x = obj.x / data.tilewidth
            blocker_y = obj.y / data.tileheight
                
            rect = pg.Rect(blocker_x* TILE_SIZE[0],blocker_y*TILE_SIZE[1], TILE_SIZE[0],TILE_SIZE[1]*4)
        
            self.rect_next_level_trigger =rect
        
   