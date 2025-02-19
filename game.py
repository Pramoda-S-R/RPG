import pygame
import os
import sys
import json
from data.scripts.tilemap import Tilemap
from data.scripts.entity import Entity
from data.scripts.player_movement import PlayerMovement
from data.scripts.menu import TitleScreen
from data.scripts.menu import GameMenu
import data.scripts.utils as Util

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.init_screen()
        self.init_assets()
        self.init_player()
        self.init_menu()
        self.load_keybinds()
        self.clock = pygame.time.Clock()
        self.state = 'TITLE'
        self.transition = False
        self.last_keypress = pygame.time.get_ticks()

    def init_screen(self):
        self.screen_width, self.screen_height = 960, 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.text_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.text_surface.set_alpha(180)
        zoom = 4
        self.game_width, self.game_height = self.screen_width // zoom, self.screen_height // zoom
        self.display = pygame.Surface((self.game_width, self.game_height))

    def init_assets(self):
        self.outdoor_spec = {
            'path': os.path.join('assets', 'tileset', 'GaiaCompiled.png'),
            'map': os.path.join('data', 'levels', 'collision_test.json'),
            'tilesize': 16,
            'columns': 8
        }
        self.background = Tilemap(
            pygame.image.load(self.outdoor_spec['path']),
            self.outdoor_spec['map'],
            self.outdoor_spec['tilesize'],
            self.outdoor_spec['columns']
        )

    def init_player(self):
        self.player_spec = {
            'path': os.path.join('assets', 'characters', 'player.png'),
            'map': os.path.join('data', 'characters', 'player.json'),
            'size': (16, 32),
            'keyframes': 4
        }
        spawn_point = {'x': 10, 'y': 16}
        self.player_pos = {'x': (self.game_width // 2) - (self.player_spec['size'][0] // 2),
                           'y': (self.game_height // 2) - (self.player_spec['size'][1] - 8)}
        self.player = Entity(
            pygame.image.load(self.player_spec['path']),
            self.player_spec['map'],
            self.player_spec['size'],
            self.player_spec['keyframes'],
            'down', 0
        )
        self.movement_handler = PlayerMovement(
            self.player, self.background, self.outdoor_spec['tilesize'], 1, False,
            Util.get_tile_cords(self.game_width, self.game_height, self.background.tile_size, spawn_point)
        )

    def init_menu(self):
        self.title_screen = TitleScreen()
        self.menu = GameMenu("data/utils/menu.json", False, 0)

    def load_keybinds(self):
        with open('data/player_data/keybinds.json') as f:
            self.keybind = json.load(f)


    def ow_game(self):
        # Rendering
        self.background.render_collisions(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])
        self.background.render_map(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])
        self.player.render_entity(self.display, self.player.facing, self.player.keyframe, self.player_pos)
        self.background.render_foreground(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])
        if self.menu.is_open:
            self.menu.render(self.text_surface, self.screen_width, self.screen_height)
        
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Scale display surface to screen size
        if self.menu.is_open:
            self.screen.blit(self.text_surface, (0, 0))
        
        # Movement only needed in OW
        if not self.menu.is_open:
            self.movement()

    def movement(self) -> None:
        keys = pygame.key.get_pressed()
        direction = None

        if not self.movement_handler.moving:
            if keys[self.keybind["up"]]: direction = "up"
            elif keys[self.keybind["left"]]: direction = "left"
            elif keys[self.keybind["down"]]: direction = "down"
            elif keys[self.keybind["right"]]: direction = "right"

        if self.movement_handler.camera != self.movement_handler.target_camera or direction:
            self.movement_handler.move_player(direction)



    def run(self) -> None:
        while True:
            self.screen.fill((0, 0, 0))
            self.display.fill((0, 0, 0))

            if self.state == "TITLE":
                self.title_screen.render(self.screen)
            elif self.state == "GAME":
                if self.transition:
                    Util.fade_out(self.screen, self.display, speed=5)
                    self.ow_game()
                    Util.fade_in(self.screen, self.display, speed=5)
                    self.transition = False
                self.ow_game()

            pygame.display.update()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

    def handle_keydown(self, event):
        if self.state == "TITLE":
            if event.key == pygame.K_UP:
                self.title_screen.current_option = (self.title_screen.current_option - 1) % len(self.title_screen.options)
            elif event.key == pygame.K_DOWN:
                self.title_screen.current_option = (self.title_screen.current_option + 1) % len(self.title_screen.options)
            elif event.key == pygame.K_RETURN:
                self.state, self.transition = self.title_screen.select_option(self.title_screen.current_option)

        elif self.state == "GAME":
            if event.key == pygame.K_ESCAPE:
                self.menu.is_open = not self.menu.is_open

            if self.menu.is_open:
                if event.key == pygame.K_UP:
                    self.menu.scroll_up()
                if event.key == pygame.K_DOWN:
                    self.menu.scroll_down()
                if event.key == pygame.K_RETURN:
                    self.menu.select_option()


                

if  __name__ == "__main__":
    game = Game()
    game.run()