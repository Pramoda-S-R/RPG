import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def get_tile_cords(game_width, game_height, tilesize, tile):
    posx = (tile['x'] * tilesize) - (game_width // 2 - 8)
    posy = (tile['y'] * tilesize) - (game_height // 2)
    return {'x': posx, 'y': posy}

def fade_in(screen, fade_surface, speed=1):
    for alpha in range(0, 255, speed):  # Increase alpha from 0 to 255
        fade_surface.set_alpha(alpha)
        screen.fill(BLACK)  # Assuming the target screen is white for this example
        screen.blit(pygame.transform.scale(fade_surface, screen.get_size()), (0,0))
        pygame.display.update()
        pygame.time.delay(10)

# Function to perform the fade out (from screen to black)
def fade_out(screen, fade_surface, speed=1):
    for alpha in range(255, -1, -speed):  # Decrease alpha from 255 to 0
        fade_surface.set_alpha(alpha)
        screen.fill(BLACK)  # Fill the screen with what you want to show after fade
        screen.blit(pygame.transform.scale(fade_surface, screen.get_size()), (0,0))
        pygame.display.update()
        pygame.time.delay(10)