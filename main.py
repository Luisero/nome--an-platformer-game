from settings import *
import time
import pytmx

import pytmx.util_pygame
from Entities.Tilemap import Tilemap
from Entities.Level import Level
from Entities.Camera import Camera

class Game:
    def __init__(self):
        pg.init()
        self.level_number = 0
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN,vsync=True)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)  # Fonte para exibir o FPS
        pg.mouse.set_visible(False) # Hide cursor here


        self.level = Level(self.level_number)

        self.aim_img= pg.image.load('Assets/Sprites/aim.png').convert_alpha()
        self.aim_img = pg.transform.scale(self.aim_img, (self.aim_img.get_width()*1.5,self.aim_img.get_height()*1.5))

       
        self.prev_time = time.time()
        self.dt = 0
        self.target_fps = TARGET_FPS
        self.fps = FPS

        
        

    def draw_aim(self):
        pos = pg.mouse.get_pos()
        pos = vec2(pos)
        pos.x -= self.aim_img.get_width()
        pos.y -= self.aim_img.get_height()
    
        self.screen.blit(self.aim_img,pos)
    def exit(self):
        pg.quit()
        exit_process()
    def change_level(self):
        self.level_number+=1
        self.level = Level(self.level_number)
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
        
        if self.level.should_change_level:
            self.change_level()

        self.level.update(self.dt)


       
   
        
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.level.camera.custom_draw(self.screen)

        rect = pg.Rect(self.level.rect_next_level_trigger)
        rect.left -= self.level.camera.scroll.x
        rect.top -= self.level.camera.scroll.y
        pg.draw.rect(self.screen,(255,0,0),rect,2)
        self.draw_aim()
        # Exibir FPS na tela
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        # Exibir posição do scroll da câmera
        scroll_text = self.font.render(f"Scroll: {self.level.camera.scroll}", True, (255, 255, 255))
        self.screen.blit(scroll_text, (10, 50))

        life_text = self.font.render(f'Life: {self.level.player.life}', True, 'white')
        self.screen.blit(life_text,(10,100))
        
    def run(self):
        self.runnig = True 
        while self.runnig:
            self.check_events()
            self.update()
            self.draw()
        
            

            

            self.clock.tick(self.target_fps)
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
