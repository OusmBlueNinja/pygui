import sys
import pygame
import pygui

# Initialize Pygame and pygui
pygui.init_pygui()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move Object with Sliders")
clock = pygame.time.Clock()

# Create a global window stack
window_stack = []

# Create sliders inside a window to control the x and y position
slider_x = pygui.Slider((20, 50), (200, 20), min_value=0, max_value=WIDTH, start_value=WIDTH // 2)
slider_y = pygui.Slider((20, 100), (200, 20), min_value=0, max_value=HEIGHT, start_value=HEIGHT // 2)

label_x = pygui.Label("X: ", (20, 35), 15)
label_y = pygui.Label("Y: ", (20, 85), 15)

knob = pygui.Knob((25,150), 40, 0, 105.5, 1, 1)

fps_label = pygui.Label("FPS: ", (5, 50), 20)
position_label = pygui.Label("POS: ", (5, 70), 20)
color_label = pygui.Label("COL: ", (5, 90), 20)



# Create windows and add them to the window stack
window = pygui.Window("Move Object", (600, 50), (250, 150), elements=[label_x, label_y, slider_x, slider_y])
debug_window = pygui.Window("Info", (0, 0), (150, HEIGHT), elements=[fps_label, position_label, color_label, knob], fixed=True)

# Add windows to the global window stack
window_stack.append(window)
window_stack.append(debug_window)

# Object to move (a rectangle)
object_pos = [WIDTH // 2, HEIGHT // 2]
object_size = (50, 50)


DEBUG = True

def handle_window_focus():
    """Handle window focus by bringing clicked windows to the top."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    if mouse_click:
        # Check if any window is clicked and bring it to the front
        for win in reversed(window_stack):  # Reverse to prioritize top-most window
            if win.rect.collidepoint(mouse_pos) and not win.fixed:
                window_stack.remove(win)  # Remove window from its current position
                window_stack.append(win)  # Move window to the end (top of the stack)
                break

def draw_gui():
    # Handle window focus before drawing
    handle_window_focus()

    # Draw windows based on their stacking order (first window is drawn first, last window is drawn last)
    for win in window_stack:
        win.call(screen)

    # Update the labels based on object position
    label_x.text = "X: " + str(object_pos[0])
    label_y.text = "Y: " + str(object_pos[1])

    # Get the values of the sliders
    object_pos[0] = int(slider_x.value)  # Update x position based on the x-slider
    object_pos[1] = int(slider_y.value)  # Update y position based on the y-slider
    
    # Update and display FPS
    fps_label.text = "FPS: " + str(round(clock.get_fps(), 1))
    position_label.text = "POS: " + str(object_pos)
    color_label.text = "COL: " + str(((20 * knob.angle/ 10), 255-(20 * knob.angle/ 10), 0))
    

while True:
    screen.fill((30, 30, 30))  # Clear screen with a dark gray color

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygui.quit_pygui()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                DEBUG = not DEBUG
    # Draw the object (rectangle)
    pygame.draw.rect(screen, ((20 * knob.angle/ 10), 255-(20 * knob.angle/ 10), 0), (*object_pos, *object_size))
    
    

    
    
    

    # Draw the GUI
    if DEBUG:
        draw_gui()

    pygame.display.flip()
    clock.tick()
