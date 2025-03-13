from settings import *
import time
from Entities.Tilemap import Tilemap
from Entities.Player import Player
from Entities.Camera import Camera

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN,vsync=True)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)  # Fonte para exibir o FPS

        self.camera = Camera()
        self.tilemap = Tilemap('./Data/Levels/0.tmx')
        self.camera.add(self.tilemap.sprites())
        self.entities_group = pg.sprite.Group()
        self.tilemap.load_tiles()

        self.prev_time = time.time()
        self.dt = 0
        self.target_fps = TARGET_FPS
        self.fps = FPS
        self.player = self.tilemap.add_player(self.camera)
        self.enemies = pg.sprite.Group()
        self.tilemap.add_enemies(self.camera, self.enemies)
        
        self.camera.add(self.player)
        self.entities_group.add(self.player)

    def exit(self):
        pg.quit()
        exit_process()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
            
        #FPS = 60
        self.fps = 60
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_ESCAPE]:
            self.exit()
        if self.keys[pg.K_g]:
            self.fps = 30
        
    def update(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.dt *= self.target_fps
        self.prev_time = now


        self.tilemap.update()
        self.enemies.update(self.dt)
        self.entities_group.update(self.dt)

        self.camera.add(self.player.bullets)

        self.camera.update_scroll(self.player.rect)
        
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.camera.custom_draw(self.screen)

        # Exibir FPS na tela
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        # Exibir posição do scroll da câmera
        scroll_text = self.font.render(f"Scroll: {self.camera.scroll}", True, (255, 255, 255))
        self.screen.blit(scroll_text, (10, 50))
        
    def run(self):
        self.runnig = True 
        while self.runnig:
            self.check_events()
            self.update()
            self.draw()
        
            

            

            self.clock.tick(self.fps)
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
