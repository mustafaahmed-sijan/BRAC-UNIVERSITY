# 🌧️ House in Rainfall | PyOpenGL Simulation

A computer graphics project developed using **Python and OpenGL (PyOpenGL)**. This project simulates a rainy environment featuring a house, trees, ground, and animated raindrops. Users can interact with the simulation to change the environment from night to day and control the direction of rainfall.

---

## 1. Simulation / Demo

### Project Preview

The simulation displays a house surrounded by trees during continuous rainfall.

**Main features:**
- 🌙 Night-to-day environment transition.
- 🌧️ 200 randomly generated animated raindrops.
- 🌬️ Interactive rain direction control.
- 🏠 House with walls, roof, door, and windows.
- 🌳 Trees and ground.
- ⚡ Real-time animation using the OpenGL idle callback.

### Keyboard Controls

| Key | Action |
|---|---|
| `D` | Increase brightness (Night → Day) |
| `N` | Decrease brightness (Day → Night) |
| `←` Left Arrow | Bend rainfall towards the left |
| `→` Right Arrow | Bend rainfall towards the right |

**Control Explanation:**

- Press `D` repeatedly to increase the sky brightness.
- Press `N` repeatedly to make the sky darker.
- Press the left arrow to increase the leftward rain slant.
- Press the right arrow to increase the rightward rain slant.

The brightness is restricted between `0.0` and `1.0`, while the rain shift is restricted between `-20` and `20`.

---

## 2. Theory

### 2.1 Computer Graphics

Computer graphics is the process of creating visual images using computers.

In this project, we use OpenGL to draw 2D objects inside a graphical window. These objects are constructed using basic geometric shapes such as triangles and rectangles.

### 2.2 OpenGL

OpenGL is a graphics API that allows programmers to render 2D and 3D graphics.

This project uses PyOpenGL, which provides Python bindings for OpenGL.

Important OpenGL concepts used:

| Concept | Purpose |
|---|---|
| `GL_TRIANGLES` | Draw triangular shapes |
| `GL_LINES` | Draw lines, including window frames and rain |
| `glColor3f()` | Set the drawing color |
| `glVertex2f()` | Define 2D vertex coordinates |
| `glBegin()` | Start drawing a primitive |
| `glEnd()` | Finish drawing a primitive |
| `glClear()` | Clear the previous frame |
| `glClearColor()` | Set the background color |
| `glMatrixMode()` | Select the matrix to modify |

### 2.3 Coordinate System

The simulation uses a coordinate system where:

- X-axis represents horizontal movement.
- Y-axis represents vertical movement.
- The center of the scene is approximately `(0, 0)`.
- The visible scene is designed around coordinates from `-250` to `250`.

The house, trees, ground, and raindrops are positioned using these coordinates.

### 2.4 Geometric Transformations

The project uses coordinate positioning to construct different objects.

For example:

- A triangle is created using three vertices.
- A rectangle is constructed using two triangles.
- Rain movement is achieved by changing the X and Y coordinates of each raindrop.

### 2.5 Animation Theory

Animation is created by continuously updating object positions.

Each raindrop has:
- An X-coordinate.
- A Y-coordinate.
- An individual falling speed.

During every animation update:

1. The Y-coordinate decreases.
2. The X-coordinate changes according to the rain direction.
3. If a raindrop reaches the ground, it is repositioned at the top.
4. The screen is refreshed to display the updated positions.

This creates the effect of continuous rainfall.

### 2.6 Color and Brightness

OpenGL uses RGB color values.

`glColor3f(R, G, B)` defines the red, green, and blue components, each ranging from `0.0` to `1.0`.

The background brightness is controlled using:

```python
glClearColor(brightness * 0.53,
             brightness * 0.81,
             brightness * 0.92, 0)
```

When brightness is `0.0`, the background becomes black.

When brightness is `1.0`, the background becomes light blue.

---

## 3. Function-by-Function Explanation

This section explains every class and function used in the project.

### 3.1 Global Variables

```python
W_Width, W_Height = 500, 500

brightness = 0.0
rain_shift = 0.0
rain_drops = []
```

| Variable | Purpose |
|---|---|
| `W_Width` | Window width |
| `W_Height` | Window height |
| `brightness` | Controls the background brightness |
| `rain_shift` | Controls the slant and horizontal drift of rainfall |
| `rain_drops` | Stores all raindrop objects |

Initially, the brightness and rain shift are both zero, and the raindrop list is empty.

### 3.2 RainDrop Class

```python
class RainDrop:
    def __init__(self):
        self.x = random.randint(-250, 250)
        self.y = random.randint(-20, 250)
        self.speed = random.randint(3, 6)
```

**Purpose:** Creates an individual raindrop with random properties.

**How it works:**

1. Generates a random X-coordinate between `-250` and `250`.
2. Generates a random Y-coordinate between `-20` and `250`.
3. Generates a random falling speed between `3` and `6`.

Every raindrop gets its own position and speed.

This makes rainfall look more natural because all raindrops do not fall at the same speed or from the same position.

### 3.3 draw_triangle()

```python
def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
```

**Purpose:** Draws a triangle using three vertices.

**How it works:**

1. `glBegin(GL_TRIANGLES)` tells OpenGL to draw triangles.
2. Three vertices define the triangle's corners.
3. `glEnd()` finishes the drawing operation.

This function is reused to create the roof and trees.

### 3.4 draw_rectangle()

```python
def draw_rectangle(x1, y1, x2, y2):
    draw_triangle(x1, y1, x2, y1, x2, y2)
    draw_triangle(x1, y1, x2, y2, x1, y2)
```

**Purpose:** Draws a rectangle using two triangles.

**How it works:**

A rectangle is divided diagonally into two triangles.

- First triangle: Bottom-left, bottom-right, top-right.
- Second triangle: Bottom-left, top-right, top-left.

Both triangles together form one rectangle.

This function is used to draw the ground, house walls, door, and windows.

### 3.5 draw_ground()

```python
def draw_ground():
    glColor3f(0.5, 0.35, 0.1)
    draw_rectangle(-250, -250, 250, -20)
```

**Purpose:** Draws the ground.

**How it works:**

1. Sets the ground color to brown.
2. Calls `draw_rectangle()`.
3. Creates a large rectangle covering the bottom portion of the scene.

The ground extends horizontally from `-250` to `250` and vertically from `-250` to `-20`.

### 3.6 draw_trees()

```python
def draw_trees():
    glColor3f(0.0, 0.7, 0.0)

    for x in range(-240, 250, 40):
        if -110 < x < 110:
            continue

        draw_triangle(x - 20, -20,
                      x + 20, -20,
                      x, 30)
```

**Purpose:** Draws multiple green trees.

**How it works:**

1. Sets the tree color to green.
2. Uses a `for` loop to generate tree positions.
3. The X-coordinate increases by 40 each time.
4. Checks whether the position is inside the house area.
5. If the position is between `-110` and `110`, `continue` skips that iteration.
6. Otherwise, a triangle is drawn to represent a tree.

**Why use `continue`?**

It prevents trees from being drawn behind or over the central house area.

### 3.7 draw_house()

```python
def draw_house():
```

**Purpose:** Draws the complete house using basic geometric shapes.

The function contains several drawing operations.

**A. House Walls**

```python
glColor3f(1.0, 1.0, 0.8)
draw_rectangle(-90, -20, 90, 70)
```

- Sets a light cream color.
- Draws the main rectangular structure of the house.

**B. Roof**

```python
glColor3f(0.4, 0.3, 0.7)
draw_triangle(-100, 70, 100, 70, 0, 130)
```

- Sets the roof color to purple.
- Uses a triangle to create the roof.

**C. Door**

```python
glColor3f(0.2, 0.5, 0.9)
draw_rectangle(-15, -20, 15, 35)
```

- Sets the door color to blue.
- Draws a rectangular door at the center.

**D. Windows**

```python
glColor3f(0.3, 0.6, 0.9)
draw_rectangle(-70, 10, -35, 45)
draw_rectangle(35, 10, 70, 45)
```

- Sets the window color to light blue.
- Creates two rectangular windows on opposite sides of the door.

**E. Window Crosses**

```python
glColor3f(0, 0, 0)
glLineWidth(2)
glBegin(GL_LINES)
```

The window crosses are created using black lines.

- Vertical lines divide each window into two sections.
- Horizontal lines divide each window into upper and lower sections.
- `glLineWidth(2)` sets the line thickness.

### 3.8 draw_rain()

```python
def draw_rain():
    glColor3f(0.4, 0.5, 1.0)
    glLineWidth(1)
    glBegin(GL_LINES)

    for d in rain_drops:
        glVertex2f(d.x, d.y)
        glVertex2f(d.x + rain_shift, d.y - 15)

    glEnd()
```

**Purpose:** Draws all the raindrops.

**How it works:**

1. Sets the rain color to light blue.
2. Sets the line thickness to 1.
3. Loops through every raindrop in `rain_drops`.
4. Uses two vertices to draw each raindrop as a line.

**Rain slant logic:**

The starting point is:

```python
(d.x, d.y)
```

The ending point is:

```python
(d.x + rain_shift, d.y - 15)
```

When `rain_shift = 0`, the rain falls vertically.

When `rain_shift` is negative, the line tilts towards the left.

When `rain_shift` is positive, the line tilts towards the right.

### 3.9 keyboardListener()

```python
def keyboardListener(key, x, y):
    global brightness

    if key == b'd':
        brightness = round(min(1.0, brightness + 0.1), 1)

    if key == b'n':
        brightness = round(max(0.0, brightness - 0.1), 1)

    glutPostRedisplay()
```

**Purpose:** Controls the background brightness through keyboard input.

**How it works:**

- `global brightness` allows the function to modify the global variable.
- Pressing `D` increases brightness by `0.1`.
- Pressing `N` decreases brightness by `0.1`.
- `min(1.0, ...)` prevents brightness from exceeding `1.0`.
- `max(0.0, ...)` prevents brightness from going below `0.0`.
- `round(..., 1)` keeps one decimal place.
- `glutPostRedisplay()` requests a new screen drawing.

**Important:** This function changes the sky brightness only, not the colors of the house, trees, or ground.

### 3.10 specialKeyListener()

```python
def specialKeyListener(key, x, y):
    global rain_shift

    if key == GLUT_KEY_LEFT:
        rain_shift = max(-20, rain_shift - 2)

    if key == GLUT_KEY_RIGHT:
        rain_shift = min(20, rain_shift + 2)

    glutPostRedisplay()
```

**Purpose:** Controls the direction of rainfall using the arrow keys.

**How it works:**

- `GLUT_KEY_LEFT` detects the left arrow.
- Pressing left decreases `rain_shift` by 2.
- `GLUT_KEY_RIGHT` detects the right arrow.
- Pressing right increases `rain_shift` by 2.
- `max(-20, ...)` prevents the value from going below `-20`.
- `min(20, ...)` prevents the value from exceeding `20`.

The rain direction is controlled by changing the global `rain_shift` variable.

### 3.11 display()

```python
def display():
    glClearColor(brightness * 0.53,
                 brightness * 0.81,
                 brightness * 0.92, 0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 200,
              0, 0, 0,
              0, 1, 0)

    draw_ground()
    draw_trees()
    draw_house()
    draw_rain()

    glutSwapBuffers()
```

**Purpose:** Renders the complete scene on the screen.

This is the main drawing function of the project.

**Execution sequence:**

1. Sets the background color based on brightness.
2. Clears the previous frame.
3. Selects the model-view matrix.
4. Resets the current model-view transformation using `glLoadIdentity()`.
5. Sets the camera position using `gluLookAt()`.
6. Draws the ground.
7. Draws the trees.
8. Draws the house.
9. Draws the rainfall.
10. Uses `glutSwapBuffers()` to display the completed frame.

**Why use double buffering?**

Double buffering allows one buffer to be displayed while another is being drawn. After rendering, the buffers are swapped to reduce visible flickering.

### 3.12 animate()

```python
def animate():
    for d in rain_drops:
        d.y -= d.speed
        d.x += rain_shift * 0.1

        if d.y < -20:
            d.y = 250
            d.x = random.randint(-250, 250)

        if d.x > 250:
            d.x = -250

        if d.x < -250:
            d.x = 250

    glutPostRedisplay()
```

**Purpose:** Updates the position of every raindrop to create continuous rainfall.

**How it works:**

**Step 1: Vertical movement**

```python
d.y -= d.speed
```

The Y-coordinate decreases according to the individual speed of each raindrop.

**Step 2: Horizontal movement**

```python
d.x += rain_shift * 0.1
```

The X-coordinate changes according to the selected rain direction.

**Step 3: Reset after reaching the ground**

```python
if d.y < -20:
    d.y = 250
    d.x = random.randint(-250, 250)
```

When a raindrop goes below the ground level:

- Its Y-coordinate is reset to `250`.
- A new random X-coordinate is generated.

This makes the raindrop fall again from the top.

**Step 4: Horizontal boundary checking**

```python
if d.x > 250:
    d.x = -250

if d.x < -250:
    d.x = 250
```

If a raindrop moves outside the horizontal boundary, it reappears from the opposite side.

**Step 5: Refresh the screen**

```python
glutPostRedisplay()
```

Requests another screen update so that the movement becomes visible.

### 3.13 init()

```python
def init():
    glClearColor(0, 0, 0, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(104, 1, 1, 1000.0)

    for i in range(200):
        rain_drops.append(RainDrop())
```

**Purpose:** Initializes the OpenGL environment and creates the raindrops.

**How it works:**

1. Sets the initial background color to black.
2. Selects the projection matrix.
3. Resets the projection matrix.
4. Sets the perspective projection using `gluPerspective()`.
5. Creates 200 raindrop objects using a `for` loop.
6. Appends each object to the `rain_drops` list.

**Perspective parameters:**

| Parameter | Value | Meaning |
|---|---:|---|
| Field of View | 104 | Camera viewing angle |
| Aspect Ratio | 1 | Width divided by height |
| Near Plane | 1 | Nearest visible depth |
| Far Plane | 1000 | Farthest visible depth |

---

## 4. Complete Code Logic

This section explains how all components work together.

### 4.1 Program Execution Flow

The program follows this execution sequence:

1. Import OpenGL libraries and Python's random module.
2. Define global variables.
3. Define the `RainDrop` class.
4. Define all drawing and control functions.
5. Initialize the GLUT environment.
6. Create the graphical window.
7. Call `init()` to configure OpenGL and generate 200 raindrops.
8. Register the display callback.
9. Register the animation callback.
10. Register keyboard and special-key callbacks.
11. Start the main event loop using `glutMainLoop()`.

### 4.2 Rainfall Algorithm

The rainfall algorithm is based on continuous coordinate updates.

**Algorithm:**

```text
START

Create 200 raindrop objects

REPEAT continuously:

    FOR each raindrop:

        Decrease Y-coordinate by its speed

        Update X-coordinate using rain_shift

        IF Y-coordinate < -20:
            Set Y-coordinate = 250
            Generate a new random X-coordinate

        IF X-coordinate > 250:
            Set X-coordinate = -250

        IF X-coordinate < -250:
            Set X-coordinate = 250

    Refresh the screen

END REPEAT
```

### 4.3 Day and Night Algorithm

```text
IF user presses D:
    brightness = brightness + 0.1
    Maximum brightness = 1.0

IF user presses N:
    brightness = brightness - 0.1
    Minimum brightness = 0.0

Update the background color
Refresh the screen
```

### 4.4 Rain Direction Algorithm

```text
IF LEFT arrow is pressed:
    rain_shift = rain_shift - 2
    Minimum rain_shift = -20

IF RIGHT arrow is pressed:
    rain_shift = rain_shift + 2
    Maximum rain_shift = 20

Update rainfall direction
Refresh the screen
```

### 4.5 How the Functions Connect

| Function | Connected Function | Relationship |
|---|---|---|
| `draw_rectangle()` | `draw_triangle()` | Uses two triangles to create a rectangle |
| `draw_ground()` | `draw_rectangle()` | Uses a rectangle to create the ground |
| `draw_trees()` | `draw_triangle()` | Uses triangles to create trees |
| `draw_house()` | `draw_rectangle()`, `draw_triangle()` | Uses geometric shapes to construct the house |
| `draw_rain()` | `rain_drops` | Reads raindrop positions and draws rain lines |
| `keyboardListener()` | `brightness` | Changes the sky brightness |
| `specialKeyListener()` | `rain_shift` | Changes the rainfall direction |
| `display()` | All drawing functions | Renders the complete scene |
| `animate()` | `rain_drops` | Updates raindrop positions |
| `init()` | `RainDrop()` | Creates 200 raindrop objects |

### 4.6 Important Logic to Understand

**Why do we use a list for raindrops?**

Because the project needs to manage 200 individual raindrops. A list allows us to store and iterate through all the objects easily.

**Why does every raindrop have a different speed?**

Random speeds create natural-looking rainfall instead of making all raindrops move together.

**Why do we reset the Y-coordinate to 250?**

When a raindrop reaches the ground, it needs to start falling again from the top.

**Why do we use `glutIdleFunc(animate)`?**

It tells GLUT to call the animation function whenever the application is idle, allowing the raindrops to move continuously.

**Why do we use `glutPostRedisplay()`?**

It requests a new frame to be rendered after a change in the scene.

**Why do we use `global` inside the keyboard functions?**

Because `brightness` and `rain_shift` are global variables, and the event-handler functions need to modify their values.

---

## 5. Project Structure

```text
House-in-Rainfall/
│
├── main.py
├── README.md
└── screenshots/
    └── simulation.png
```

*The folder structure is a suggested organization. The Python file can have any name.*

---

## 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PyOpenGL | OpenGL integration with Python |
| OpenGL | Rendering geometric shapes and graphics |
| GLUT | Window management, keyboard input, and animation |
| GLU | Camera and perspective configuration |
| Random | Generating random raindrop positions and speeds |

---

## 7. Installation and Execution

### Requirements

- Python 3
- PyOpenGL
- PyOpenGL_accelerate (optional)
- A compatible OpenGL environment

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Folder

```bash
cd House-in-Rainfall
```

### Step 3: Install Dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Step 4: Run the Project

```bash
python main.py
```

The graphical window will open, and the rainfall simulation will start automatically.

---

## 8. Key Learning Outcomes

Through this project, I explored:

- Basic OpenGL rendering.
- Drawing geometric shapes using vertices.
- Constructing complex objects from simple shapes.
- Working with RGB color models.
- Implementing keyboard event handling.
- Creating real-time animation.
- Using object-oriented programming.
- Managing multiple animated objects using lists.
- Applying coordinate-based movement.
- Implementing boundary detection and object repositioning.

---

## 9. Conclusion

The House in Rainfall project demonstrates how basic geometric shapes, object-oriented programming, randomization, and real-time animation can be combined to create an interactive computer graphics simulation.

The project provides three main interactive features: continuous rainfall, adjustable rain direction, and day-night brightness control.

It also demonstrates how OpenGL and Python can be used together to build a simple but interactive graphical environment.

---

**Project:** House in Rainfall  
**Language:** Python  
**Graphics Library:** PyOpenGL  
**Category:** Computer Graphics  
**Rendering:** Real-Time Animation

