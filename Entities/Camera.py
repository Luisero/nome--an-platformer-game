from settings import *
from math import sin

class Camera(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.scroll = vec2(-97,3097)
        
    

    def update_scroll(self, rect:pg.Rect):
        true_scroll_x,true_scroll_y = self.scroll.x , self.scroll.y
        true_scroll_x += (rect.x - self.scroll.x - (SCREEN_WIDTH/2+rect.width))/20
        true_scroll_y += (rect.y - self.scroll.y - (SCREEN_HEIGHT/2))/40

        self.scroll = vec2(int(true_scroll_x), int(true_scroll_y))
        
    def custom_draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface, self.scroll)