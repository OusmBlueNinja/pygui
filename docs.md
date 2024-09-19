# **PyGUI Documentation**

## **1. Initialization and Cleanup**

You must initialize `pygui` before use and quit when you're done with the library.

### **Initialization:**

```python
import pygui

# Initialize PyGUI
pygui.init_pygui()
```

### **Cleanup:**

```python
# When you're done with PyGUI
pygui.quit_pygui()
```

---

### **2. Button**

A button that can detect mouse clicks.

#### **Constructor:**

```python
pygui.Button(text, pos, size)
```

- **text**: `str` - The text displayed on the button.
- **pos**: `tuple(int, int)` - The position of the button `(x, y)`.
- **size**: `tuple(int, int)` - The size of the button `(width, height)`.

#### **Example:**

```python
button = pygui.Button("Click Me", (100, 100), (200, 50))

if button.call(screen):
    print("Button clicked!")
```

---

### **3. Slider**

A slider allows the user to adjust a value between a minimum and maximum range.

#### **Slider Constructor:**

```python
pygui.Slider(pos, size, min_value=0, max_value=100, start_value=50)
```

- **pos**: `tuple(int, int)` - The position of the slider `(x, y)`.
- **size**: `tuple(int, int)` - The size of the slider `(width, height)`.
- **min_value**: `float` - Minimum value of the slider.
- **max_value**: `float` - Maximum value of the slider.
- **start_value**: `float` - The initial value of the slider.

#### **Slider Example:**

```python
slider = pygui.Slider((100, 200), (200, 20), min_value=0, max_value=10, start_value=5)
current_value = slider.call(screen)
print(f"Slider Value: {current_value}")
```

---

### **4. Checkbox**

A checkbox element allows for toggling between checked and unchecked states.

#### **Checkbox Constructor:**

```python
pygui.Checkbox(label, pos, checked=False)
```

- **label**: `str` - The label displayed next to the checkbox.
- **pos**: `tuple(int, int)` - The position of the checkbox `(x, y)`.
- **checked**: `bool` - Initial state of the checkbox (default is `False`).

#### **Checkbox Example:**

```python
checkbox = pygui.Checkbox("Enable Feature", (100, 250), checked=True)

if checkbox.call(screen):
    print(f"Checkbox state: {checkbox.checked}")
```

---

### **5. TextInput**

A text input field that allows users to type text.

#### **TextInput Constructor:**

```python
pygui.TextInput(pos, size, initial_text="")
```

- **pos**: `tuple(int, int)` - The position of the text input field `(x, y)`.
- **size**: `tuple(int, int)` - The size of the input box `(width, height)`.
- **initial_text**: `str` - The initial text inside the input field (default is an empty string).

#### **TextInput Example:**

```python
text_input = pygui.TextInput((100, 300), (200, 40), initial_text="Hello!")

text_value = text_input.call(screen, event_list)
print(f"Text Input Value: {text_value}")
```

---

### **6. Label**

A label is a simple text display.

#### **Label Constructor:**

```python
pygui.Label(text, pos, font_size=24, color=(255, 255, 255))
```

- **text**: `str` - The text displayed in the label.
- **pos**: `tuple(int, int)` - The position of the label `(x, y)`.
- **font_size**: `int` - The font size (default is 24).
- **color**: `tuple(int, int, int)` - The color of the text `(R, G, B)`.

#### **Label Example:**

```python
label = pygui.Label("This is a label", (100, 50))

label.call(screen)
```

---

### **7. Window**

A window element that can contain multiple GUI elements, such as sliders, buttons, and checkboxes.

#### **Window Constructor:**

```python
pygui.Window(title, pos, size, elements=None, fixed=False)
```

- **title**: `str` - The title of the window.
- **pos**: `tuple(int, int)` - The position of the window `(x, y)`.
- **size**: `tuple(int, int)` - The size of the window `(width, height)`.
- **elements**: `list` - A list of GUI elements to be included in the window.
- **fixed**: `bool` - Whether the window can be moved by the user (default is `False`).

#### **Window Example:**

```python
window = pygui.Window("My Window", (100, 100), (300, 200), elements=[button, slider, checkbox])

window.call(screen)
```

---

### **Example Usage**

Here’s an example of how you can combine these elements into a basic GUI:

```python
import pygame
import pygui

# Initialize Pygame and PyGUI
pygui.init_pygui()
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Create GUI elements
button = pygui.Button("Click Me", (100, 100), (200, 50))
slider = pygui.Slider((100, 200), (200, 20), min_value=0, max_value=10, start_value=5)
checkbox = pygui.Checkbox("Enable Feature", (100, 250), checked=True)
label = pygui.Label("This is a label", (100, 50))
window = pygui.Window("Control Window", (400, 100), (300, 400), elements=[button, slider, checkbox, label])

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Clear the screen with a dark color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the window and its elements
    window.call(screen)

    # Update display
    pygame.display.flip()

# Quit PyGUI and Pygame
pygui.quit_pygui()
pygame.quit()
```
