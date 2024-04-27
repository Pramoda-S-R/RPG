import pygame
import sys
import json
from data.scripts.tilemap import Tilemap
from data.scripts.entity import Entity
from data.scripts.player_movement import PlayerMovement
from data.scripts.menu import TitleScreen
import data.scripts.utils as Util

class Game():
    def __init__(self) -> None:
        pygame.init()
        # Surface initialization
        self.screen_width , self.screen_height = 960, 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        zoom = 4  # 2 for 32x32 or 4 for 16x16 tileset
        self.game_width = self.screen_width // zoom
        self.game_height = self.screen_height // zoom
        self.display = pygame.Surface((self.game_width, self.game_height))

        # Load assets and create tilemap object
        self.outdoor_spec = {'path': 'assets/tileset/GaiaCompiled.png', 
                             'map': 'data/levels/collision_test.json', 
                             'tilesize': 16, 
                             'columns': 8}
        self.background = Tilemap(pygame.image.load(self.outdoor_spec['path']), self.outdoor_spec['map'], self.outdoor_spec['tilesize'], self.outdoor_spec['columns'])

        # Temporary init state
        spawn_point = {'x': 10, 'y': 16}
        
        # Player NOTE: Currently configured for only 4 and 8 max keyframes
        self.player_spec = {'path': 'assets/characters/player.png', 
                       'map': 'data/characters/player.json', 
                       'size': (16, 32), 
                       'keyframes': 4}
        self.player_pos = {'x': (self.game_width // 2) - (self.player_spec['size'][0] // 2), 'y': (self.game_height // 2) - (self.player_spec['size'][1] - 8)}
        self.player = Entity(pygame.image.load(self.player_spec['path']), self.player_spec['map'], self.player_spec['size'], self.player_spec['keyframes'], 'down', 0)

        # Movement Handler
        self.movement_handler = PlayerMovement(self.player, self.background, self.outdoor_spec['tilesize'], 1, False, Util.get_tile_cords(self.game_width, self.game_height, self.background.tile_size, spawn_point))

        # Title
        self.title_screen = TitleScreen()
        self.transition = False

        # Game state
        self.state = 'TITLE'

        # TODO: Implement key binding system
        keybind = 'data/player_data/keybinds.json'
        with open(keybind) as f:
            self.keybind = json.load(f)

        # Clock
        self.clock = pygame.time.Clock()


    def ow_game(self):
        # Rendering
        self.background.render_collisions(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])
        self.background.render_map(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])
        self.player.render_entity(self.display, self.player.facing, self.player.keyframe, self.player_pos)
        self.background.render_foreground(self.display, self.movement_handler.camera['x'], self.movement_handler.camera['y'])

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Scale display surface to screen size

        # Movement only needed in OW
        self.movement()


    def movement(self) -> None:
        keys = pygame.key.get_pressed()
        direction = None
        if not self.movement_handler.moving:
            if keys[self.keybind["up"]]:
                direction = "up"
            elif keys[self.keybind["left"]]:
                direction = "left"
            elif keys[self.keybind["down"]]:
                direction = "down"
            elif keys[self.keybind["right"]]:
                direction = "right"
        if self.movement_handler.camera != self.movement_handler.target_camera or direction:
            self.movement_handler.move_player(direction)


    def run(self) -> None:
        while True:
            if not self.transition:
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
                    if self.state == "TITLE":
                        if event.key == pygame.K_UP:
                            self.title_screen.current_option = (self.title_screen.current_option - 1) % len(self.title_screen.options)
                        elif event.key == pygame.K_DOWN:
                            self.title_screen.current_option = (self.title_screen.current_option + 1) % len(self.title_screen.options)
                        elif event.key == pygame.K_RETURN:
                            self.state, self.transition = self.title_screen.select_option(self.title_screen.current_option)
                

if  __name__ == "__main__":
    game = Game()
    game.run()