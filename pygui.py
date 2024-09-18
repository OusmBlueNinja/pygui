import pygame, math, os, json

# Load colors from the JSON file
def _load_colors(file_path='pygui_colors.json'):
    """Load the colors from the JSON configuration file."""
    colors = {"label_colors":{},"gui_color":{}, "slider_color":{}}
    if not os.path.exists(file_path):
        print(f"[pygui] Color configuration file '{file_path}' not found.")
    else:
        with open(file_path, 'r') as file:
            colors = json.load(file)
    return colors

# Load the colors at the start of the program
color = {"label_colors":{},"gui_color":{}, "slider_color":{}} # Default colors

def init_pygui():
    """Initialize Pygame."""
    global windowsId, colors
    
    colors = _load_colors()
    
    windowsId = 0
    pygame.init()

def quit_pygui():
    """Quit Pygame."""
    pygame.quit()

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.is_clicked = False
        self.mouse_released = True  # Track mouse state internally
        self.type = Button

    def call(self, screen):
        """Draw the button and check if it's clicked."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Colors
        base_color = (70, 70, 70)
        hover_color = (100, 100, 100)
        click_color = (150, 150, 150)
        color = base_color

        if self.rect.collidepoint(mouse_pos):
            color = hover_color
            if mouse_click and self.mouse_released:
                color = click_color
                self.is_clicked = True
                self.mouse_released = False  # Mark that the mouse is now pressed
            else:
                self.is_clicked = False
        else:
            self.is_clicked = False

        # Reset mouse_released when the mouse button is released
        if not mouse_click:
            self.mouse_released = True

        pygame.draw.rect(screen, color, self.rect)

        # Render text
        font = pygame.font.SysFont(None, 24)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        return self.is_clicked


class Checkbox:
    def __init__(self, label, pos, checked=False):
        self.label = label
        self.pos = pos
        self.rect = pygame.Rect(pos, (20, 20))
        self.checked = checked
        self.mouse_released = True  # Track mouse state internally
        
        self.type = Checkbox

    def call(self, screen):
        """Draw the checkbox and toggle its state if clicked."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Handle toggle only on mouse click
        if self.rect.collidepoint(mouse_pos):
            if mouse_click and self.mouse_released:
                self.checked = not self.checked
                self.mouse_released = False  # Mark that the mouse is pressed

        # Reset mouse_released when the mouse button is released
        if not mouse_click:
            self.mouse_released = True

        # Draw checkbox
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        if self.checked:
            pygame.draw.line(screen, (255, 255, 255), self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(screen, (255, 255, 255), self.rect.topright, self.rect.bottomleft, 2)

        # Draw label
        label_font = pygame.font.SysFont(None, 24)
        label_surf = label_font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, (self.rect.right + 10, self.rect.y))

        return self.checked


class TextInput:
    def __init__(self, pos, size, initial_text=""):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.text = initial_text
        self.is_active = False

    def call(self, screen, event_list):
        """Draw the text input field and handle typing when active."""
        base_color = (255, 255, 255)
        active_color = (230, 230, 255)
        color = active_color if self.is_active else base_color

        # Draw the input box
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Handle clicking to activate/deactivate input
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos):
            self.is_active = True
        elif pygame.mouse.get_pressed()[0] and not self.rect.collidepoint(mouse_pos):
            self.is_active = False

        # Handle text input
        if self.is_active:
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

        # Render text
        font = pygame.font.SysFont(None, 24)
        text_surf = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) / 2))

        return self.text



class Slider:
    def __init__(self, pos, size, min_value=0, max_value=100, start_value=0):
        self.pos = pos  # Relative position inside the window
        self.size = size  # Size of the slider (track size)
        self.min_value = min_value  # Minimum value of the slider
        self.max_value = max_value  # Maximum value of the slider
        self.value = start_value  # Current value of the slider
        self.type = Slider

        # Calculate knob position and size
        self.knob_width = 10  # Width of the knob
        self.rect = pygame.Rect(pos, size)  # Track rectangle (relative to the window)
        self.knob_rect = pygame.Rect(pos[0], pos[1], self.knob_width, size[1])  # Knob rectangle

        self.dragging = False  # Track whether the knob is being dragged
        
        self.knob_color = colors['slider_color'].get("knob_color", (255,255,255))
        self.backround_color = colors['slider_color'].get("background", (150,150,150))

        # Update the knob position based on the initial value
        self.update_knob_position()

    def update_knob_position(self):
        """Update the knob's position based on the current value."""
        # Calculate the knob's x position based on the value
        knob_x = int(self.rect.x + ((self.value - self.min_value) / (self.max_value - self.min_value)) * (self.rect.width - self.knob_width))
        self.knob_rect.x = knob_x  # Set the knob's x position

    def call(self, screen):
        """Draw the slider and handle user interaction."""
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        mouse_click = pygame.mouse.get_pressed()[0]  # Check if the mouse button is pressed
        
        # Draw the slider track
        pygame.draw.rect(screen, self.backround_color, self.rect)

        # Draw the knob
        pygame.draw.rect(screen, self.knob_color, self.knob_rect)
        
        self.move()

        # Handle dragging logic
        if self.dragging:
            if mouse_click:
                # Move the knob as the mouse moves
                new_x = max(self.rect.x, min(mouse_pos[0] - self.knob_width // 2, self.rect.x + self.rect.width - self.knob_width))
                self.knob_rect.x = new_x

                # Update the value based on the knob's new position
                self.value = self.min_value + ((self.knob_rect.x - self.rect.x) / (self.rect.width - self.knob_width)) * (self.max_value - self.min_value)
            else:
                # Stop dragging when the mouse button is released
                self.dragging = False
        elif self.knob_rect.collidepoint(mouse_pos) and mouse_click:
            # Start dragging if the mouse clicks on the knob
            self.dragging = True

        # Ensure the value is clamped within bounds
        self.value = max(self.min_value, min(self.value, self.max_value))

        return self.value  # Return the current value of the slider

    def move(self):
        """Update the slider's position based on the window's position."""
        # Update the slider's main rect position relative to the window's position

        # Correctly set the knob's y position to match the track and window
        self.knob_rect.y = self.rect.y  # Align the knob's y position with the track's y position

        # Update the knob's x position relative to the track
        self.update_knob_position()


class Knob:
    def __init__(self, center, radius, min_angle=-135, max_angle=135, start_angle=0, sensitivity=1):
        self.pos = center  # Center of the knob (x, y)
        self.radius = radius  # Radius of the knob
        self.min_angle = min_angle  # Minimum rotation angle (in degrees)
        self.max_angle = max_angle  # Maximum rotation angle (in degrees)
        self.angle = start_angle  # Initial angle (in degrees)
        self.sensitivity = sensitivity  # Sensitivity of knob rotation

        # Create a rect based on the position and radius of the knob
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (self.pos[0] - self.radius, self.pos[1] - self.radius)  # Set the center of the rect to the knob's center

        self.dragging = False  # Track if the knob is being dragged
        self.last_mouse_y = None  # To track the previous mouse y-position
        self.type = Knob

    def call(self, screen):
        """Draw the knob and handle rotation."""
        # Get the current mouse position and mouse click status
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Check if the knob is clicked (or already being dragged)
        if self.dragging:
            if not mouse_click:  # Stop dragging if mouse is released
                self.dragging = False
            else:
                # Calculate the change in mouse Y and rotate the knob accordingly
                if self.last_mouse_y is not None:
                    mouse_y_delta = mouse_pos[1] - self.last_mouse_y
                    self.angle -= mouse_y_delta * self.sensitivity  # Rotate angle based on vertical mouse movement

                # Ensure the angle is clamped between min_angle and max_angle
                self.angle = max(self.min_angle, min(self.angle, self.max_angle))

            self.last_mouse_y = mouse_pos[1]  # Update the last Y position of the mouse

        # Check for initial click to start dragging
        elif self.rect.collidepoint(mouse_pos) and mouse_click:
            self.dragging = True
            self.last_mouse_y = mouse_pos[1]  # Start dragging, save the initial mouse Y position

        # Draw the knob (as a circle)
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius, 2)

        # Draw the rect around the knob for debugging purposes
        #pygame.draw.rect(screen, (0, 255, 255), self.rect, 1)

        # Draw a "needle" to indicate the current angle
        needle_length = self.radius - 10
        needle_angle_rad = math.radians(self.angle)
        needle_x = self.rect.center[0] + needle_length * math.cos(needle_angle_rad)
        needle_y = self.rect.center[1] - needle_length * math.sin(needle_angle_rad)
        pygame.draw.line(screen, (255, 0, 0), self.rect.center, (needle_x, needle_y), 3)

        return self.angle

    def move(self, new_pos):
        """Move the knob to a new position."""
        self.pos = new_pos  # Update the position
        # Update the rect's center to match the new position of the knob
        self.rect.center = (self.pos[0] - self.radius, self.pos[1] - self.radius)

        
        

        
        
        
class Window:
    focused_window = None  # Class-level variable to track the currently focused window

    def __init__(self, title:str, pos:tuple|pygame.Vector2, size:int, elements=None, fixed=False):
        global windowsId
        self.title = title
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.is_dragging = False
        self.drag_offset = (0, 0)
        self.elements = elements if elements else []  # Store elements as part of the window
        self.header_height = 30  # Header for dragging the window
        
        self.fixed = fixed
        
        self.id = windowsId 
        windowsId += 1
        
        for element in self.elements:
            element.rect.topleft = (self.pos[0] + element.pos[0], self.pos[1] + element.pos[1])
            
        self.title_text_color = colors['gui_color'].get("title_text", (255,255,255))
        self.backround_color = colors['gui_color'].get("background", (70,70,70))
        self.title_color = colors['gui_color'].get("title", (100,100,100))

    def draw(self, screen):
        """Draw the window and allow it to be dragged."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        
        if not self.fixed:
            # Check if this window is clicked and should become the focused window
            if self.rect.collidepoint(mouse_pos) and mouse_click and Window.focused_window is None:
                Window.focused_window = self  # Set this window as the focused window
    
            # Handle dragging if this window is the focused one
            if Window.focused_window == self:
                if self.is_dragging:
                    if mouse_click:
                        self.pos = (mouse_pos[0] - self.drag_offset[0], mouse_pos[1] - self.drag_offset[1])
                        self.rect.topleft = self.pos
                    else:
                        self.is_dragging = False
                        Window.focused_window = None  # Release focus when dragging stops
                elif pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.header_height).collidepoint(mouse_pos) and mouse_click:
                    self.is_dragging = True
                    self.drag_offset = (mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])

        # Draw the window (but only allow interaction if it's the focused window)
        pygame.draw.rect(screen, self.backround_color, self.rect)
        pygame.draw.rect(screen, self.title_color, (self.pos[0], self.pos[1], self.size[0], self.header_height))

        # Draw title text
        font = pygame.font.SysFont(None, 24)
        title_surf = font.render(self.title, True, self.title_text_color)
        screen.blit(title_surf, (self.pos[0] + 5, self.pos[1] + 5))

    def move_element(self, element):
        """Move the element according to the window's position, only if this window is focused."""
        if Window.focused_window == self or not Window.focused_window:
            element.rect.topleft = (self.pos[0] + element.pos[0], self.pos[1] + element.pos[1])

    def call(self, screen):
        """Draw the window and all contained elements."""
        self.draw(screen)  # Draw the window itself
        # Always draw all elements inside the window
        for element in self.elements:
            self.move_element(element)
            element.call(screen)
            #print(element.type, self.id)




class Label:
    def __init__(self, text, pos, font_size=24, color_name="default", ):
        self.text = text  # The label text
        self.pos = pos  # The position of the label (relative to the window)
        self.font_size = font_size  # Font size
        self.color = colors['label_colors'].get(color_name, (255,255,255))

        # Create a font object
        self.font = pygame.font.SysFont(None, self.font_size)

        # Create a rect based on the label's position and text size
        self.rect = self.font.render(self.text, True, self.color).get_rect(topleft=self.pos)
        
        self.type = Label

    def call(self, screen):
        """Render and draw the label text."""
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect.topleft)  # Draw the label using the rect position

if __name__ == "__main__":
    print("[pygui] Import this file into your project to use, dont run directly")
else:
    print("[pygui] Py-GUI 0.4.1")