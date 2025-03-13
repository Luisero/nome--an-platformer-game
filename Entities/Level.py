from settings import *
import time
from Entities.Camera import Camera
from Entities.Player import Player
from Entities.Tilemap import Tilemap


class Level:
    def __init__(self, number):
        self.number = number
        self.camera = Camera()
        self.tilemap = Tilemap(f'./Data/Levels/0.tmx')
        self.camera.add(self.tilemap.sprites())
        self.entities_group = pg.sprite.Group()
        self.tilemap.load_tiles()

        
        
        self.player = self.tilemap.add_player(self.camera)
        self.enemies = pg.sprite.Group()
        self.tilemap.add_enemies(self.camera, self.enemies)

        self.enemy_blockers = []
        self.add_enemy_blockers()
        for enemy in self.enemies.sprites():
            enemy.load_blockers(self.enemy_blockers)
        self.camera.add(self.player)
        self.entities_group.add(self.player)

    
    
        
    def update(self):
       


        self.tilemap.update()
        self.enemies.update(self.dt)
        self.entities_group.update(self.dt)

        self.camera.add(self.player.bullets)

        self.camera.update_scroll(self.player.rect)
        for enemy in self.enemies:
            enemy.get_player_pos(self.player.position)
            self.camera.add(enemy.bullets)

        

        if self.player.position.y > 6000:
            self.exit()

    
    def add_enemy_blockers(self):
        data = pytmx.load_pygame('./Data/Levels/0.tmx', pixelalpha=True)

        for obj in data.get_layer_by_name('Enemy blockers'):
            blocker_x = obj.x / data.tilewidth
            blocker_y = obj.y / data.tileheight
                
            rect = pg.Rect(blocker_x* TILE_SIZE[0],blocker_y*TILE_SIZE[1], TILE_SIZE[0],TILE_SIZE[1])
            
            self.enemy_blockers.append(rect)
        
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.camera.custom_draw(self.screen)

        # Exibir FPS na tela
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        # Exibir posição do scroll da câmera
        scroll_text = self.font.render(f"Scroll: {self.camera.scroll}", True, (255, 255, 255))
        self.screen.blit(scroll_text, (10, 50))