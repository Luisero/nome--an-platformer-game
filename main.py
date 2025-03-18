from settings import *
import math
import time
import pytmx
import pytmx.util_pygame
import moderngl
import array
from Entities.Tilemap import Tilemap
from Entities.Level import Level
from Entities.Camera import Camera

class Game:
    def __init__(self):
        pg.init()
        self.level_number = 0
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF,vsync=True)
        self.displa_shad = pg.surface.Surface(self.screen.get_size())
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)  # Fonte para exibir o FPS
        pg.mouse.set_visible(False) # Hide cursor here
        self.time = 0
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array.array(f'f',[
            -1.0, 1.0, 0.0, 0.0,
             1.0, 1.0, 1.0, 0.0,
            -1.0,-1.0, 0.0, 1.0,
             1.0,-1.0, 1.0, 1.0,
        ]))

        self.vert_shader = '''
        #version 330 core
        in vec2 vert;
        in vec2 texcoord;

        out vec2 uvs;
        
        void main()
        {
            uvs = texcoord; 
            gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
        }
        '''

        self.frag_shader = '''
            #version 330 core
            uniform sampler2D tex;
            uniform vec2 player_pos;
            uniform vec2 screen_size;
            uniform float radius;
            in vec2 uvs;
            out vec4 f_color;

            void main()
            {
                float warp = 0.7;
                vec2 uv = uvs;

                // Distorção por curvatura para simular o efeito CRT
                float curvature = sin(uv.x * 6.0) * 0.05;  // Ajuste o valor para distorcer a tela
                uv.x += curvature;

                // Calculando o efeito de vinheta (escurecimento nas bordas)
                vec2 screen_uvs = uv * screen_size;
                vec2 norm_pos = player_pos / screen_size;
                float dist = length(screen_uvs - norm_pos * screen_size) / (radius * length(screen_size));
                float vignette = smoothstep(1.0, 0.5, dist);
                
                // Aplicando o efeito de scanlines (linhas horizontais)
                float scanlines = abs(sin(gl_FragCoord.y) * 0.5 * 0.75);  // Ajuste para mais ou menos scanlines
                
                // Amostrando a textura e aplicando os efeitos de vinheta e scanlines
                vec4 color = texture(tex, uv);
                f_color = vec4(color.rgb * vignette * (1.0 - scanlines), color.a);
            

            }
        '''

        self.shader_prog = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)

        self.render_obj = self.ctx.vertex_array(self.shader_prog,[(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.level = Level(self.level_number)

        self.aim_img= pg.image.load('Assets/Sprites/aim.png').convert_alpha()
        self.aim_img = pg.transform.scale(self.aim_img, (self.aim_img.get_width()*1.5,self.aim_img.get_height()*1.5))

       
        self.prev_time = time.time()
        self.dt = 0
        self.target_fps = TARGET_FPS
        self.fps = FPS

        self.tex = self.surf_to_texture()
        
    def surf_to_texture(self):
        tex =  self.ctx.texture(self.screen.get_size(),4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(self.screen.get_view('1'))
        return tex

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


       
   
        
    def draw_debugs_texts(self):
        # Exibir FPS na tela
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        # Exibir posição do scroll da câmera
        scroll_text = self.font.render(f"Scroll: {self.level.camera.scroll}", True, (255, 255, 255))
        self.screen.blit(scroll_text, (10, 50))

        life_text = self.font.render(f'Life: {self.level.player.life}', True, 'white')
        self.screen.blit(life_text,(10,100))
    def draw(self):
        self.displa_shad.fill(BG_COLOR)
        self.screen.fill(BG_COLOR)
        self.level.camera.custom_draw(self.screen)

        rect = pg.Rect(self.level.rect_next_level_trigger)
        rect.left -= self.level.camera.scroll.x
        rect.top -= self.level.camera.scroll.y
        pg.draw.rect(self.screen,(255,0,0),rect,2)

        self.draw_debugs_texts()

        self.draw_aim()
        self.displa_shad.blit(self.screen)

        
        
    def run(self):
        self.runnig = True 
        while self.runnig:
            self.check_events()
            self.update()
            self.draw()
            self.time+=1        
            camera_player_pos = self.level.player.position - self.level.camera.scroll
            self.shader_prog['screen_size'] = (float(SCREEN_SIZE[0]), float(SCREEN_SIZE[1]))
            self.shader_prog['player_pos'] = (float(camera_player_pos[0]), float(camera_player_pos[1]))
            self.shader_prog['radius'] = 0.5
            

            
            frame_tex = self.surf_to_texture()
            frame_tex.use(0)
            self.shader_prog['tex'] = 0     
            
            self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)
            self.clock.tick(self.target_fps)
            pg.display.flip()

            frame_tex.release()

if __name__ == '__main__':
    game = Game()
    game.run()
