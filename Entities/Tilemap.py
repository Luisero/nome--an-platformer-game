import pytmx
import pygame as pg
import pytmx.util_pygame
from Entities.Tile import Tile
from Entities.Player import Player
from Entities.Enemy import Enemy
from Entities.Capacitor import Capacitor
from Entities.Coin import Coin
from settings import *


class Tilemap(pg.sprite.Group):
    def __init__(self, filename, initial_pos=vec2(0, 0)) -> None:
        super().__init__()  # Inicializa o grupo de sprites
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.collideable_tiles = pg.sprite.Group()
        self.initial_pos = initial_pos
        self.load_tiles()

    def load_tiles(self):
        """Carrega os tiles do mapa e os adiciona ao grupo de sprites."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    image = self.tmx_data.get_tile_image_by_gid(gid)
                    attributes = self.tmx_data.get_tile_properties_by_gid(gid) or {
                    }

                    position = vec2(
                        x * TILE_SIZE[0]+self.initial_pos.x, y * TILE_SIZE[1] + self.initial_pos.y)
                    collide = attributes.get(
                        'collide', False)  # Evita KeyError

                    if collide:
                        collide = True

                    if image:

                        image = pg.transform.scale(image, TILE_SIZE)
                        tile = Tile(position=position, surface=image,
                                    group=self, collide=collide)
                        if collide:
                            self.collideable_tiles.add(tile)

    def add_enemies(self, camera_group, enemy_group):
        for object in self.tmx_data.get_layer_by_name('Enemies'):

            if object.type == 'basic':

                # Ajuste da posição Y (compensação da origem do Tiled)
                enemy_x = (object.x + self.initial_pos.x) / \
                    self.tmx_data.tilewidth
                enemy_y = (object.y + self.initial_pos.y) / \
                    self.tmx_data.tileheight

                enemy = Enemy(
                    vec2(enemy_x * TILE_SIZE[0], enemy_y*TILE_SIZE[1]), self)
                enemy_group.add(enemy)
                camera_group.add(enemy)

    def get_coins(self, camera, player):
        coins = list()
        for object in self.tmx_data.get_layer_by_name('Pickables'):
            if object.name == 'Coin':
                coin_x = (object.x + self.initial_pos.x) / \
                    self.tmx_data.tilewidth
                coin_y = (object.y + self.initial_pos.y) / \
                    self.tmx_data.tileheight

                coin = Coin(
                    vec2(coin_x*TILE_SIZE[0], coin_y*TILE_SIZE[1]), player, camera)
                coins.append(coin)
        return coins

    def add_traps(self, camera, traps_group, player):
        traps_layer = self.tmx_data.get_layer_by_name('Traps')
        if traps_layer:
            for object in self.tmx_data.get_layer_by_name('Traps'):

                if object.type == 'capacitor':

                    # Ajuste da posição Y (compensação da origem do Tiled)
                    trap_x = (object.x + self.initial_pos.x) / \
                        self.tmx_data.tilewidth
                    trap_y = (object.y + self.initial_pos.y) / \
                        self.tmx_data.tileheight

                    trap = Capacitor(
                        vec2(trap_x * TILE_SIZE[0], trap_y*TILE_SIZE[1]), camera, player)
                    camera.add(trap.animation)
                    traps_group.add(trap)

    def add_player(self, camera_group):
        object = self.tmx_data.get_object_by_name('player')

        # Ajuste da posição Y (compensação da origem do Tiled)
        player_x = (object.x + self.initial_pos.x) / self.tmx_data.tilewidth
        player_y = (object.y + self.initial_pos.y) / self.tmx_data.tileheight

        player = Player(
            vec2(player_x * TILE_SIZE[0], player_y*TILE_SIZE[1]), self, camera_group)
        camera_group.add(player)
        return player

    def draw(self, surface):
        """Desenha os tiles na superfície fornecida."""
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)

    def get_collision_with(self, sprite):
        colliisions = []
        for tile in self.collideable_tiles.sprites():

            if tile.rect.colliderect(sprite.rect):
                colliisions.append(tile)
        # return pg.sprite.spritecollide(sprite, self, False)

        return colliisions
    # unused

    def make_map(self):
        """Cria uma superfície com o mapa renderizado."""
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.render(temp_surface)
        return temp_surface
