from settings import *


class Explosion(pg.sprite.Sprite):
    def __init__(self, pos, camera, speed=0.1):
        super().__init__()

        self.pos = pos
        self.images =[]
        self.current_frame=0

        self.speed= speed

        camera.add(self)
        self.load_images()
        self.pos.x -= self.images[0].get_width()/2
        self.pos.y -= self.images[0].get_height()/2

    def load_images(self):
        for i in range(74):
            image = pg.image.load(f'Assets/Sprites/Explosion/frame00{i:02d}.png').convert_alpha()
            image = pg.transform.scale2x(image)
            image = pg.transform.scale2x(image)
            self.images.append(image)

        

    def update(self):
        self.current_frame+=self.speed
        if self.current_frame > len(self.images)-1:
            self.kill()

    def draw(self, surface,scroll):
        pos = self.pos - scroll

        surface.blit(self.images[int(self.current_frame)],pos)