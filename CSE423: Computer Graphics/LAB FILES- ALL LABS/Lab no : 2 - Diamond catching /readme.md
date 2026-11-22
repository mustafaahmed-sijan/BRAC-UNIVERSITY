# 💎 Catch the Diamonds! | CSE423 Computer Graphics

A 2D interactive game developed using **Python, PyOpenGL, and GLUT** as part of the CSE423 Computer Graphics Lab Assignment 2.

The objective is simple: control a catcher at the bottom of the screen and catch falling diamonds to increase your score. The game implements the **Midpoint Line Drawing Algorithm with 8-zone conversion**, AABB collision detection, real-time animation, and an automatic Cheat Mode.

---

# 1. Simulation / Gameplay

## 🎮 Game Overview

The game window has a falling diamond, a catcher, and three interactive buttons.

**Main gameplay features:**

- 💎 Randomly generated falling diamonds.
- 🎯 Player-controlled catcher.
- 🧮 Midpoint Line Drawing Algorithm for drawing all game objects.
- 🌈 Random diamond colors.
- 📈 Gradually increasing diamond speed.
- 🤖 Automatic Cheat Mode.
- ⏸️ Pause and resume functionality.
- 🔄 Restart functionality.
- ❌ Exit button.
- 🏆 Score tracking and Game Over detection.

## Game Controls

| Control | Action |
|---|---|
| `←` Left Arrow | Move catcher left |
| `→` Right Arrow | Move catcher right |
| `C` or `c` | Toggle Cheat Mode |
| Restart Button | Restart the game |
| Play/Pause Button | Pause or resume |
| Exit Button | Close the game |

## Gameplay Rules

1. A diamond starts falling from a random horizontal position.
2. The player moves the catcher using the left and right arrow keys.
3. If the diamond touches the catcher, the score increases by 1.
4. A new diamond appears at the top with a random color.
5. The falling speed gradually increases as time passes.
6. If the diamond reaches the bottom without being caught, the game ends.
7. The catcher changes to red when the game is over.

## Simulation Screenshot

Add your actual game screenshot here after running the program.

```markdown
![Catch the Diamonds Gameplay](screenshots/gameplay.png)
```

## Recommended Screenshots

| Screenshot | What to Capture |
|---|---|
| `gameplay.png` | Normal gameplay |
| `cheat-mode.png` | Automatic catcher movement |
| `game-over.png` | Red catcher after losing |
| `paused.png` | Paused game |

---

# 2. Theory

This project demonstrates several important concepts of computer graphics.

## 2.1 Midpoint Line Drawing Algorithm

The Midpoint Line Drawing Algorithm is a rasterization algorithm used to draw straight lines on a pixel-based display.

Instead of calculating every point using floating-point equations, it uses an integer decision parameter to determine which pixel should be selected next.

The algorithm is particularly efficient because it mainly uses integer addition and subtraction.

### Why do we need the Midpoint Algorithm?

In this assignment, the game objects must be drawn using the Midpoint Line Drawing Algorithm.

Therefore, we cannot simply use ordinary OpenGL lines to draw the diamond, catcher, or buttons.

Instead, we calculate the individual pixel coordinates and render them using:

```python
glBegin(GL_POINTS)
```

Each calculated coordinate represents one pixel.

## 2.2 Understanding the Eight Zones

A line can have eight different directions depending on its slope and the direction of its endpoints.

These directions are divided into eight zones.

<escape>
             Zone 2 | Zone 1
                    |
             Zone 3 | Zone 0
          ----------+----------
             Zone 4 | Zone 7
                    |
             Zone 5 | Zone 6
</escape>

The main idea is that the Midpoint Algorithm is easiest to implement in Zone 0.

Zone 0 has these properties:

- X increases.
- Y increases or remains constant.
- The slope is between 0 and 1.
- The line moves more horizontally than vertically.

Instead of implementing eight separate algorithms, this project converts every line into Zone 0, draws it, and converts the points back to their original zone.

### Eight-Zone Characteristics

| Zone | Direction | Characteristics |
|---|---|---|
| 0 | Right and upward | Positive slope, 0 to 1 |
| 1 | Upward and right | Positive slope, greater than 1 |
| 2 | Upward and left | Negative X, positive Y |
| 3 | Left and upward | Negative X, positive slope |
| 4 | Left and downward | Negative X, negative Y |
| 5 | Downward and left | Steep negative slope |
| 6 | Downward and right | Negative Y, negative X |
| 7 | Right and downward | Negative slope, between -1 and 0 |

## 2.3 Zone 0 Midpoint Algorithm

For Zone 0:

Let:

- `dx = x2 - x1`
- `dy = y2 - y1`

The initial decision parameter is:

\[
d = 2dy-dx
\]

Two possible movements exist:

**East (E):**

\[
incE=2dy
\]

The next pixel is:

\[
(x+1,y)
\]

**North-East (NE):**

\[
incNE=2(dy-dx)
\]

The next pixel is:

\[
(x+1,y+1)
\]

### Decision Logic

```python
if d > 0:
    d += incNE
    y += 1
else:
    d += incE
```

- If `d > 0`, choose the North-East pixel.
- Otherwise, choose the East pixel.

The X-coordinate increases in every iteration.

This process continues until the ending X-coordinate is reached.

## 2.4 Zone Conversion

The algorithm converts coordinates from their original zone into Zone 0.

For example:

- Zone 0: `(x, y)`
- Zone 1: `(y, x)`
- Zone 2: `(y, -x)`
- Zone 3: `(-x, y)`
- Zone 4: `(-x, -y)`
- Zone 5: `(-y, -x)`
- Zone 6: `(-y, x)`
- Zone 7: `(x, -y)`

After drawing the line in Zone 0, the coordinates are converted back into their original zone.

This makes one algorithm capable of drawing lines in all eight directions.

## 2.5 AABB Collision Detection

AABB stands for **Axis-Aligned Bounding Box**.

It is a collision detection technique that checks whether two rectangular bounding boxes overlap.

In this project:

- The diamond is represented by its bounding rectangle.
- The catcher is represented by its bounding rectangle.

For the diamond:

\[
D_L=x_d-\frac{size}{2}
\]

\[
D_R=x_d+\frac{size}{2}
\]

\[
D_T=y_d+\frac{size}{2}
\]

\[
D_B=y_d-\frac{size}{2}
\]

For the catcher:

\[
C_L=x_c-\frac{width}{2}
\]

\[
C_R=x_c+\frac{width}{2}
\]

\[
C_T=y_c+15
\]

\[
C_B=y_c
\]

Collision occurs when all four conditions are true:

\[
D_L<C_R
\]

\[
D_R>C_L
\]

\[
D_B<C_T
\]

\[
D_T>C_B
\]

If all conditions are satisfied, the diamond and catcher overlap.

**Important:** The collision detection uses rectangular bounding boxes, not the exact diamond and bowl outlines.

## 2.6 Delta Time and Animation

Delta time represents the time elapsed between two consecutive animation updates.

\[
\Delta t=currentTime-lastTime
\]

Instead of moving objects by a fixed number of pixels per frame, the game uses:

\[
Movement=Speed\times\Delta t
\]

For example, if:

- Speed = 100 pixels/second
- Delta time = 0.02 seconds

Then:

\[
Movement=100\times0.02=2\ pixels
\]

This makes the animation less dependent on the computer's frame rate.

## 2.7 Game State Management

The project uses three game states:

| State | Description |
|---|---|
| `playing` | Normal gameplay |
| `paused` | Game temporarily stopped |
| `game_over` | Player has missed a diamond |

The game state determines whether the game logic should execute.

For example:

```python
if game_state != "playing":
    return
```

When the game is paused or over, the update function stops modifying gameplay variables.

## 2.8 Cheat Mode

Cheat Mode automatically moves the catcher toward the falling diamond.

It uses the difference between the diamond's X-coordinate and the catcher's X-coordinate.

\[
difference=diamond_x-catcher_x
\]

Movement is calculated using:

\[
movement=600\times\Delta t
\]

If the difference is positive, the catcher moves right.

If the difference is negative, the catcher moves left.

If the difference is small enough, the catcher directly aligns with the diamond.

The diamond is temporarily held at Y-coordinate 80 if the catcher has not yet reached the required horizontal position.

This gives the automatic catcher time to move into position.

---

# 3. Function-by-Function Explanation

This section explains every function and how it contributes to the game.

## 3.1 Global Variables

```python
game_state = "playing"
score = 0
catcher_x = 250
catcher_width = 60
catcher_speed = 200
cheat_mode = False
```

These variables manage the main game state.

| Variable | Purpose |
|---|---|
| `game_state` | Controls whether the game is playing, paused, or over |
| `score` | Stores the number of diamonds caught |
| `catcher_x` | Horizontal position of the catcher |
| `catcher_width` | Width of the catcher |
| `catcher_speed` | Normal catcher movement speed |
| `cheat_mode` | Enables or disables automatic catching |

### Diamond Variables

```python
diamond_x = random.randint(50, 450)
diamond_y = 480
diamond_size = 20
diamond_speed = 100
```

- `diamond_x`: Random horizontal starting position.
- `diamond_y`: Initial vertical position.
- `diamond_size`: Size of the diamond.
- `diamond_speed`: Initial falling speed.

The diamond color is generated using three random RGB values:

```python
diamond_color = [
    random.uniform(0.45, 1.0),
    random.uniform(0.45, 1.0),
    random.uniform(0.45, 1.0)
]
```

Each component represents red, green, and blue.

### Time Variables

```python
last_time = time.time()
speed_increase_timer = 0
```

- `last_time` stores the previous animation time.
- `speed_increase_timer` tracks the time spent in active gameplay for difficulty progression.

### Button Definitions

Three dictionaries store the position and dimensions of the buttons.

```python
restart_button = {"x": 50, "y": 450, "width": 40, "height": 30}
play_pause_button = {"x": 230, "y": 450, "width": 40, "height": 30}
exit_button = {"x": 410, "y": 450, "width": 40, "height": 30}
```

These coordinates are used both for drawing and mouse-click detection.

## 3.2 find_zone()

```python
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return 0

    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx <= 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6
```

**Purpose:** Determines which of the eight zones contains the line.

**Working logic:**

1. Calculate horizontal difference `dx`.
2. Calculate vertical difference `dy`.
3. Check whether both coordinates are identical.
4. Compare the absolute values of `dx` and `dy`.
5. Check the signs of `dx` and `dy`.
6. Return the appropriate zone number.

**Why use `abs()`?**

Because we need to compare the magnitude of horizontal and vertical movement, regardless of their direction.

**Why use `abs(dx) >= abs(dy)`?**

It identifies lines that are more horizontal than vertical.

If the vertical movement is greater, the line belongs to one of the steep zones.

## 3.3 convert_to_zone0()

```python
def convert_to_zone0(x, y, zone):
    conversions = {
        0: (x, y),
        1: (y, x),
        2: (y, -x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (-y, x),
        7: (x, -y),
    }
    return conversions[zone]
```

**Purpose:** Converts any coordinate into its equivalent Zone 0 coordinate.

**Working logic:**

1. Receives X, Y, and zone number.
2. Uses a dictionary containing eight coordinate transformations.
3. Selects the transformation corresponding to the zone.
4. Returns the converted coordinate.

For example:

If the original coordinate is:

```python
x = 5
y = 10
zone = 1
```

The conversion is:

```python
(10, 5)
```

The X and Y coordinates are swapped.

This transformation makes the steep line behave like a Zone 0 line.

## 3.4 convert_from_zone0()

```python
def convert_from_zone0(x, y, zone):
    conversions = {
        0: (x, y),
        1: (y, x),
        2: (-y, x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (y, -x),
        7: (x, -y),
    }
    return conversions[zone]
```

**Purpose:** Converts Zone 0 coordinates back to their original zone.

**Working logic:**

1. Receives a Zone 0 coordinate.
2. Checks the original zone number.
3. Applies the corresponding reverse transformation.
4. Returns the original coordinate.

**Important difference:**

- `convert_to_zone0()` transforms original coordinates into Zone 0.
- `convert_from_zone0()` restores the original coordinate system.

Both functions are necessary to draw lines in all eight directions.

## 3.5 midpoint_line_zone0()

```python
def midpoint_line_zone0(x1, y1, x2, y2):
    points = []

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    for x in range(x1, x2 + 1):
        points.append((x, y))

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

    return points
```

**Purpose:** Calculates all the pixels required to draw a line in Zone 0.

This is the core implementation of the Midpoint Line Drawing Algorithm.

**Working logic:**

1. Creates an empty list called `points`.
2. Calculates `dx` and `dy`.
3. Calculates the initial decision parameter.
4. Calculates the East increment.
5. Calculates the North-East increment.
6. Starts from the first coordinate.
7. Uses a loop to process every X-coordinate.
8. Stores the current pixel.
9. Checks the decision parameter.
10. Updates the decision parameter and Y-coordinate when necessary.
11. Returns the complete list of pixels.

### Mathematical Logic

Initial decision parameter:

\[
d=2dy-dx
\]

East increment:

\[
incE=2dy
\]

North-East increment:

\[
incNE=2(dy-dx)
\]

Decision:

```python
if d > 0:
    d += incNE
    y += 1
else:
    d += incE
```

The algorithm chooses the closest pixel to the ideal mathematical line.

**Why return a list?**

Because the next function needs all the calculated pixel coordinates before rendering them.

## 3.6 draw_line_midpoint()

```python
def draw_line_midpoint(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)

    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)

    if x1_z0 > x2_z0:
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0

    zone0_points = midpoint_line_zone0(
        x1_z0, y1_z0, x2_z0, y2_z0
    )

    glBegin(GL_POINTS)

    for x_z0, y_z0 in zone0_points:
        x_orig, y_orig = convert_from_zone0(x_z0, y_z0, zone)
        glVertex2f(x_orig, y_orig)

    glEnd()
```

**Purpose:** Draws a line in any of the eight zones using the Zone 0 midpoint algorithm.

This function connects the entire eight-zone system.

**Execution sequence:**

1. Finds the original zone.
2. Converts both endpoints into Zone 0.
3. Checks whether the endpoints need to be swapped.
4. Calls `midpoint_line_zone0()`.
5. Receives all calculated pixels.
6. Converts each pixel back to its original zone.
7. Sends every pixel to OpenGL using `glVertex2f()`.

### Why swap the coordinates?

The Zone 0 algorithm expects X to increase from the starting point to the ending point.

If the first X-coordinate is greater than the second, the endpoints are swapped.

This ensures that the algorithm processes the line in the correct direction.

### Why use GL_POINTS?

```python
glBegin(GL_POINTS)
```

Because the algorithm calculates individual pixels instead of asking OpenGL to draw a continuous line.

Each `glVertex2f()` represents one calculated pixel.

## 3.7 draw_diamond()

```python
def draw_diamond(x, y, size, color):
    glColor3f(color[0], color[1], color[2])
    half_size = size // 2

    draw_line_midpoint(x, y + half_size, x + half_size, y)
    draw_line_midpoint(x + half_size, y, x, y - half_size)
    draw_line_midpoint(x, y - half_size, x - half_size, y)
    draw_line_midpoint(x - half_size, y, x, y + half_size)
```

**Purpose:** Draws a diamond using exactly four midpoint lines.

**Working logic:**

A diamond has four important points:

- Top
- Right
- Bottom
- Left

The function connects these points using four calls to `draw_line_midpoint()`.

The color is assigned using `glColor3f()`.

The variable `half_size` determines the distance between the center and each vertex.

## 3.8 draw_catcher()

```python
def draw_catcher(x, y, width, is_game_over=False):
    if is_game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    half_width = width // 2
    height = 15

    draw_line_midpoint(x - half_width, y, x - half_width + 10, y + height)
    draw_line_midpoint(x - half_width + 10, y + height, x + half_width - 10, y + height)
    draw_line_midpoint(x + half_width - 10, y + height, x + half_width, y)
    draw_line_midpoint(x + half_width, y, x - half_width, y)
```

**Purpose:** Draws the catcher bowl using four midpoint lines.

**Working logic:**

1. Checks whether the game is over.
2. Sets the catcher color to red if the game is over.
3. Otherwise, sets the catcher color to white.
4. Calculates half of the catcher width.
5. Defines the catcher height as 15.
6. Draws four connected lines to construct the bowl.

The catcher is composed of:

- Left slanted side.
- Upper horizontal side.
- Right slanted side.
- Bottom horizontal side.

## 3.9 draw_restart_button()

```python
def draw_restart_button():
    glColor3f(0.0, 0.85, 0.8)

    x = restart_button["x"] + 20
    y = restart_button["y"] + 15

    draw_line_midpoint(x, y, x - 15, y)
    draw_line_midpoint(x - 15, y, x - 10, y + 8)
    draw_line_midpoint(x - 15, y, x - 10, y - 8)
```

**Purpose:** Draws the restart arrow.

**Working logic:**

1. Sets a teal color.
2. Calculates the center of the restart button.
3. Draws a horizontal line.
4. Draws two diagonal lines to create the arrowhead.

All three lines use the midpoint algorithm.

## 3.10 draw_play_pause_button()

```python
def draw_play_pause_button():
    glColor3f(1.0, 0.75, 0.0)

    x = play_pause_button["x"] + 20
    y = play_pause_button["y"] + 15

    if game_state == "playing":
        draw_line_midpoint(x - 5, y - 10, x - 5, y + 10)
        draw_line_midpoint(x + 5, y - 10, x + 5, y + 10)
    else:
        draw_line_midpoint(x - 8, y - 10, x + 8, y)
        draw_line_midpoint(x + 8, y, x - 8, y + 10)
        draw_line_midpoint(x - 8, y + 10, x - 8, y - 10)
```

**Purpose:** Displays the pause or play icon according to the game state.

**Working logic:**

If the game is playing:

- Draws two vertical lines.
- These lines represent the pause symbol.

If the game is paused or over:

- Draws three connected lines.
- These lines create a triangular play symbol.

The icon changes according to `game_state`.

## 3.11 draw_exit_button()

```python
def draw_exit_button():
    glColor3f(1.0, 0.0, 0.0)

    x = exit_button["x"] + 20
    y = exit_button["y"] + 15

    draw_line_midpoint(x - 10, y - 10, x + 10, y + 10)
    draw_line_midpoint(x - 10, y + 10, x + 10, y - 10)
```

**Purpose:** Draws the exit button.

**Working logic:**

1. Sets the color to red.
2. Calculates the button center.
3. Draws two diagonal lines.
4. The two lines form an X symbol.

## 3.12 check_collision()

```python
def check_collision(diamond_x, diamond_y, diamond_size,
                    catcher_x, catcher_y, catcher_width):

    d_left = diamond_x - diamond_size // 2
    d_right = diamond_x + diamond_size // 2
    d_top = diamond_y + diamond_size // 2
    d_bottom = diamond_y - diamond_size // 2

    c_left = catcher_x - catcher_width // 2
    c_right = catcher_x + catcher_width // 2
    c_top = catcher_y + 15
    c_bottom = catcher_y

    return (
        d_left < c_right
        and d_right > c_left
        and d_bottom < c_top
        and d_top > c_bottom
    )
```

**Purpose:** Determines whether the falling diamond touches the catcher.

**Working logic:**

1. Calculates the diamond's left boundary.
2. Calculates the diamond's right boundary.
3. Calculates the diamond's top and bottom boundaries.
4. Calculates the catcher's boundaries.
5. Compares both bounding boxes.
6. Returns `True` if they overlap.
7. Otherwise, returns `False`.

This function uses AABB collision detection.

**Why return multiple conditions using `and`?**

Because all four overlap conditions must be true for the two bounding boxes to intersect.

## 3.13 spawn_new_diamond()

```python
def spawn_new_diamond():
    global diamond_x, diamond_y, diamond_color

    diamond_x = random.randint(40, 460)
    diamond_y = 480

    diamond_color = [
        random.uniform(0.45, 1.0),
        random.uniform(0.45, 1.0),
        random.uniform(0.45, 1.0),
    ]
```

**Purpose:** Generates a new diamond after the previous one is caught or when the game restarts.

**Working logic:**

1. Generates a random horizontal position.
2. Resets the vertical position to 480.
3. Generates a new random RGB color.
4. Updates the global diamond variables.

The diamond always starts near the top of the screen.

## 3.14 reset_game()

```python
def reset_game():
    global game_state, score, catcher_x
    global diamond_speed, speed_increase_timer, cheat_mode

    game_state = "playing"
    score = 0
    catcher_x = 250
    diamond_speed = 100
    speed_increase_timer = 0
    cheat_mode = False

    spawn_new_diamond()
    print("Starting Over")
```

**Purpose:** Restarts the game from its initial condition.

**Working logic:**

1. Changes the game state to playing.
2. Resets the score to zero.
3. Moves the catcher to the center.
4. Resets the diamond speed.
5. Resets the speed increase timer.
6. Disables Cheat Mode.
7. Calls `spawn_new_diamond()`.
8. Prints a restart message.

This function is called when the restart button is clicked.

## 3.15 update_game()

```python
def update_game(delta_time):
```

**Purpose:** Controls the main game logic.

This is one of the most important functions because it manages:

- Diamond movement.
- Increasing difficulty.
- Cheat Mode.
- Collision detection.
- Score updates.
- Game Over conditions.

### Step 1: Check Game State

```python
if game_state != "playing":
    return
```

If the game is paused or over, the function stops immediately.

### Step 2: Increase Diamond Speed

```python
speed_increase_timer += delta_time
diamond_speed = min(220, 100 + speed_increase_timer * 4)
```

The falling speed increases gradually with elapsed gameplay time.

Mathematically:

\[
Speed=100+4t
\]

Where `t` is the accumulated active gameplay time.

The maximum speed is 220.

The `min()` function prevents the speed from exceeding the limit.

### Step 3: Cheat Mode Movement

```python
if cheat_mode:
    difference = diamond_x - catcher_x
    movement = 600 * delta_time
```

Calculates how far the catcher is from the diamond.

If the difference is small enough:

```python
if abs(difference) <= movement:
    catcher_x = diamond_x
```

The catcher directly aligns with the diamond.

Otherwise:

```python
elif difference > 0:
    catcher_x += movement
else:
    catcher_x -= movement
```

The catcher moves towards the diamond.

### Step 4: Boundary Checking

```python
if catcher_x < catcher_width // 2:
    catcher_x = catcher_width // 2
elif catcher_x > 500 - catcher_width // 2:
    catcher_x = 500 - catcher_width // 2
```

Prevents the catcher from moving outside the window.

### Step 5: Diamond Movement

```python
next_diamond_y = diamond_y - diamond_speed * delta_time
```

Calculates the next vertical position.

Since Y decreases, the diamond moves downward.

### Step 6: Cheat Mode Diamond Holding

```python
if cheat_mode and next_diamond_y <= 80 and abs(diamond_x - catcher_x) > catcher_width // 2:
    diamond_y = 80
else:
    diamond_y = next_diamond_y
```

If Cheat Mode is active and the diamond approaches the catcher before the catcher is horizontally aligned, the diamond is temporarily held at Y = 80.

Otherwise, normal falling continues.

### Step 7: Collision Detection

```python
if check_collision(diamond_x, diamond_y, diamond_size,
                   catcher_x, 50, catcher_width):

    score += 1
    print(f"Score: {score}")
    spawn_new_diamond()
```

If the diamond touches the catcher:

- Score increases by one.
- The updated score is printed.
- A new diamond appears.

### Step 8: Game Over

```python
elif diamond_y < 30:
    game_state = "game_over"
    print(f"Game Over! Final Score: {score}")
```

If the diamond falls below the specified limit without being caught, the game ends.

## 3.16 display()

```python
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if game_state != "game_over":
        draw_diamond(int(diamond_x), int(diamond_y),
                     diamond_size, diamond_color)

    draw_catcher(int(catcher_x), 50, catcher_width,
                 game_state == "game_over")

    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()

    glutSwapBuffers()
```

**Purpose:** Draws the complete game interface.

**Working logic:**

1. Clears the previous frame.
2. Resets the model-view matrix.
3. Checks whether the game is over.
4. Draws the diamond if the game is not over.
5. Draws the catcher.
6. Changes the catcher color to red if the game is over.
7. Draws the restart button.
8. Draws the play/pause button.
9. Draws the exit button.
10. Swaps the buffers to display the completed frame.

**Important:** The score is currently printed in the terminal, not rendered inside the game window.

## 3.17 animate()

```python
def animate():
    global last_time

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    if delta_time > 0.05:
        delta_time = 0.05

    update_game(delta_time)
    glutPostRedisplay()
```

**Purpose:** Continuously updates the game.

**Working logic:**

1. Gets the current time.
2. Calculates delta time.
3. Updates `last_time`.
4. Limits delta time to 0.05 seconds.
5. Calls `update_game()`.
6. Requests a new frame.

**Why limit delta time to 0.05?**

If the application becomes inactive for a while, a large time difference could cause objects to move an unexpectedly large distance.

The maximum delta time prevents this large movement.

## 3.18 keyboard_listener()

```python
def keyboard_listener(key, x, y):
```

**Purpose:** Handles keyboard input.

### Cheat Mode

```
