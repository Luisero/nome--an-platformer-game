import pytmx
import pygame as pg
import pytmx.util_pygame
from Entities.Tile import Tile
from Entities.Player import Player
from settings import *

class Tilemap(pg.sprite.Group):
    def __init__(self, filename, initial_pos = vec2(0,0)) -> None:
        super().__init__()  # Inicializa o grupo de sprites
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.initial_pos = initial_pos
        self.load_tiles()

    def load_tiles(self):
        """Carrega os tiles do mapa e os adiciona ao grupo de sprites."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    image = self.tmx_data.get_tile_image_by_gid(gid)
                    attributes = self.tmx_data.get_tile_properties_by_gid(gid) or {}

                    position = vec2(x * TILE_SIZE[0]+self.initial_pos.x, y * TILE_SIZE[1] + self.initial_pos.y)
                    #collider = attributes.get('collide', False)  # Evita KeyError
                    
                    
                    if image:
                        
                        image = pg.transform.scale(image, TILE_SIZE).convert_alpha()
                        tile = Tile(position=position, surface=image, group=self)
       
                
            
    
    def add_player(self, camera_group):
        object = self.tmx_data.get_object_by_name('player')
        
        # Ajuste da posição Y (compensação da origem do Tiled)
        player_x = (object.x + self.initial_pos.x) / self.tmx_data.tilewidth
        player_y = (object.y + self.initial_pos.y) / self.tmx_data.tileheight
        
        player = Player(vec2(player_x* TILE_SIZE[0], player_y*TILE_SIZE[1]), self)
        camera_group.add(player)
        return player


                        

    def draw(self, surface):
        """Desenha os tiles na superfície fornecida."""
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)

    def get_collision_with(self, sprite):
      
        return pg.sprite.spritecollide(sprite, self, False)

    def make_map(self):
        """Cria uma superfície com o mapa renderizado."""
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.render(temp_surface)
        return temp_surface
