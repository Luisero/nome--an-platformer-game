from settings import *
import pytmx
import pygame as pg

class Animation(pg.sprite.Sprite):
    def __init__(self, spritesheet_path, pos=vec2(0,0), repeat=True, size=vec2(TILE_SIZE[0],TILE_SIZE[1]), speed=0.1):
        self.tmx_data = pytmx.load_pygame(spritesheet_path, pixelalpha=True)
        self.repeat = repeat
        self.size = size
        self.current_frame = 0
        self.speed = speed
        self.images = self.load_images()
        self.current_image = self.images[self.current_frame] if self.images else None
        self.image = self.current_image.get_frect()

    def load_images(self):
        images = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    image = self.tmx_data.get_tile_image_by_gid(gid)
                    if image:
                        image = pg.transform.scale(image, self.size)
                        images.append(image)
        return images

    def play(self, flip=False):
        self.current_frame += self.speed
        if self.current_frame >= len(self.images):
            if self.repeat:
                self.current_frame = 0 
            else:
                self.current_frame = len(self.images) - 1  

        self.current_image = self.images[int(self.current_frame) % len(self.images)]
        self.current_image = pg.transform.flip(self.current_image,flip,False)
    def draw(self, surface,pos):
        if self.current_image:
            surface.blit(self.current_image, pos)