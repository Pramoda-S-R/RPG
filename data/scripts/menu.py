import pygame
import sys
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