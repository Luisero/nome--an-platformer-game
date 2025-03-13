# TEMPLATE: handle collisions with tilemap and load tiles with pytmx

## Tilemap
### Tile
```python
class Tile(pg.sprite.Sprite):
    def __init__(self,position, surface, group) -> None:
        super().__init__(group)
        self.image = surface
       
        self.position = position
     
        self.rect = self.image.get_rect(topleft =self.position)
```
    A basic class that contains a simple tile.Inherts of a basic sprite.

### Tilemap
```python
class Tilemap(pg.sprite.Group):
```
    Inherts from sprite group. Will contain  a group of tiles.
```python
def __init__(self, filename) -> None:
        super().__init__()  
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.load_tiles()
```