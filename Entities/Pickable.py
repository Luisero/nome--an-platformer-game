from settings import *


class Pickable(pg.sprite.Sprite):
    def __init__(self, pos: vec2):
        super().__init__()
        self.image = pg.surface.Surface(TILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.pos = pos

    def on_collected(self):
        # do somethin
        pass
