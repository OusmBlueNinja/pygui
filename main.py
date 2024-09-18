import sys
import pygame
import pygui

# Initialize Pygame and pygui
pygui.init_pygui()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move Object with Sliders")
clock = pygame.time.Clock()

# Create sliders inside a window to control the x and y position
slider_x = pygui.Slider((20, 50), (200, 20), min_value=0, max_value=WIDTH, start_value=WIDTH // 2)
slider_y = pygui.Slider((20, 100), (200, 20), min_value=0, max_value=HEIGHT, start_value=HEIGHT // 2)

label_x = pygui.Label("X: ", (20,35), 15)
label_y = pygui.Label("Y: ", (20,85), 15)


# Create a window to hold the sliders
window = pygui.Window("Move Object", (50, 50), (250, 150))

# Object to move (a rectangle)
object_pos = [WIDTH // 2, HEIGHT // 2]
object_size = (50, 50)


def draw_gui():
    # Draw and interact with the window and sliders
    window.call(screen, [slider_x, slider_y, label_x, label_y])

    # Get the values of the sliders
    object_pos[0] = int(slider_x.call(screen))  # Update x position based on the x-slider
    object_pos[1] = int(slider_y.call(screen))  # Update y position based on the y-slider
    
    pass

while True:
    screen.fill((30, 30, 30))  # Clear screen with a dark gray color

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygui.quit_pygui()
            sys.exit()
            
            
            
            
            
    
    pygame.draw.rect(screen, (0, 255, 0), (*object_pos, *object_size))

    
    
    draw_gui()
    
    
    

    pygame.display.flip()
    clock.tick(60)
