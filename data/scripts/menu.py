import pygame
import sys
import json
import data.scripts.utils as utils

class TitleScreen:
    def __init__(self):
        self.options = ["Start Game", "Controls", "Exit"]
        self.current_option = 0  # Index of the currently selected option


    def render(self, screen):
        screen.fill((3, 17, 51))  # Fill the screen with black or another background
        font = pygame.font.Font('assets/font/arial.ttf', 16)  # Choose appropriate font
        for index, option in enumerate(self.options):
            color = (255, 255, 255) if index == self.current_option else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (100, 100 + index * 40))  # Adjust positioning as needed


    def select_option(self, option_index):
        if option_index == 0:  # Start Game
            return ("GAME", True)
        elif option_index == 1:  # Controls
            self.show_controls()
        elif option_index == 2:  # Exit
            pygame.quit()
            sys.exit()    


    def show_controls(self):
        # Display controls information
        pass


class GameMenu:
    def __init__(self, menu: str, is_open: bool, selected_option: int):
        self.is_open = is_open
        with open(menu, 'r') as f:
            self.menu = json.load(f)
        self.selected_option = selected_option

    def scroll_down(self):
        if self.selected_option < len(self.menu["options"]) - 1:
            self.selected_option += 1
        else:
            self.selected_option = 0
        
    def scroll_up(self):
        if self.selected_option > 0:
            self.selected_option -= 1
        else:
            self.selected_option = len(self.menu["options"]) - 1

    def render(self, screen: pygame.Surface, width: int, height: int):
        menu_font = pygame.font.Font('assets/font/arial.ttf', 50)
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Draw menu options
        for i, option in enumerate(self.menu['options']):
            color = (255, 215, 0) if i == self.selected_option else (255, 255, 255)
            text_surface = menu_font.render(option['name'], True, color)
            screen.blit(text_surface, (3, i*50))

    def select_option(self):
        option = self.menu["options"][self.selected_option]["name"]
        if option == "Quit":
            pygame.quit()
            sys.exit()
        if option == "Settings":
            return (1440, 960)
            

if __name__ == '__main__':
    pygame.init()
    title_screen = TitleScreen()
    screen = pygame.display.set_mode((960, 640))
    display = pygame.Surface((240, 160))
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        title_screen.render(display)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()