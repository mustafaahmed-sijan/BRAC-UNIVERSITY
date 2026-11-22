# CSE423_Lab Assignment-2
# ======================= Task =============================

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Game state management
game_state = "playing"  # FSM: playing/paused/game_over
score = 0
cheat_mode = False  # toggled with the 'c' key
catcher_x = 250  # Horizontal position (center)
catcher_width = 60
catcher_speed = 350  # Movement speed (pixels/sec)

# Diamond properties
diamond_x = random.randint(50, 450)  # Random horizontal spawn
diamond_y = 480  # Start at top
diamond_size = 20
diamond_speed = 100  # Initial fall speed (pixels/sec)
diamond_acceleration = 5  # Speed gain per second (pixels/sec^2)
diamond_color = [random.random(), random.random(), random.random()]  # Random RGB

# Time tracking for frame-rate independence
last_time = time.time()

last_key_time = time.time()  # time of the previous arrow key event

# UI button definitions (position and size)
restart_button = {"x": 50, "y": 450, "width": 40, "height": 30}

play_pause_button = {"x": 230, "y": 450, "width": 40, "height": 30}

exit_button = {"x": 410, "y": 450, "width": 40, "height": 30}


# --- Midpoint 
def find_zone(x1, y1, x2, y2):
    """Zone classification for line orientation"""
    dx = x2 - x1
    dy = y2 - y1

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


def convert_to_zone0(x, y, zone):
    """Transform to Zone 0 coordinates"""
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


def convert_from_zone0(x, y, zone):
    """Inverse transform from Zone 0"""
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


def midpoint_line_zone0(x1, y1, x2, y2):
    """Core midpoint algorithm for Zone 0"""
    points = []
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = x1, y1

    for x in range(x1, x2 + 1):
        points.append((x, y))
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

    return points


def draw_line_midpoint(x1, y1, x2, y2):
    """Complete line drawing with zone handling"""
    
    zone = find_zone(x1, y1, x2, y2)
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)

    if x1_z0 > x2_z0:  # Ensure left-to-right
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0

    zone0_points = midpoint_line_zone0(x1_z0, y1_z0, x2_z0, y2_z0)

    # Render points in original coordinate system
    glBegin(GL_POINTS)
    
    for x_z0, y_z0 in zone0_points:
        
        x_orig, y_orig = convert_from_zone0(x_z0, y_z0, zone)
        
        glVertex2f(x_orig, y_orig)
    glEnd()


# --- End of Midpoint


def draw_diamond(x, y, size, color):
    """Render diamond shape using 4 midpoint lines"""
    glColor3f(color[0], color[1], color[2])
    
    half_size = size // 2

    # Draw 4 connected lines forming diamond
    draw_line_midpoint(x, y + half_size, x + half_size, y)  # Top-right
    
    draw_line_midpoint(x + half_size, y, x, y - half_size)  # Right-bottom
    
    draw_line_midpoint(x, y - half_size, x - half_size, y)  # Bottom-left
    draw_line_midpoint(x - half_size, y, x, y + half_size)  # Left-top


def draw_catcher(x, y, width, is_game_over=False):
    """Render catcher as bowl shape using 4 midpoint lines"""
    # Red for game over, white otherwise
    
    glColor3f(1.0, 0.0, 0.0) if is_game_over else glColor3f(1.0, 1.0, 1.0)

    half_width = width // 2
    height = 15

    # Draw catcher shape (trapezoid)
    draw_line_midpoint(x - half_width, y, x - half_width + 10, y + height)  # Left side
    draw_line_midpoint(
        x - half_width + 10, y + height, x + half_width - 10, y + height
    )  # Top
    draw_line_midpoint(x + half_width - 10, y + height, x + half_width, y)  # Right side
    draw_line_midpoint(x + half_width, y, x - half_width, y)  # Bottom


def draw_restart_button():
    """Render restart button (left arrow)"""
    glColor3f(0.0, 1.0, 0.9)  # Bright teal color
    x, y = restart_button["x"] + 20, restart_button["y"] + 15

    # Arrow shape: horizontal + two diagonals
    draw_line_midpoint(x, y, x - 15, y)  # Horizontal
    draw_line_midpoint(x - 15, y, x - 10, y + 8)  # Upper diagonal
    draw_line_midpoint(x - 15, y, x - 10, y - 8)  # Lower diagonal


def draw_play_pause_button():
    
    """Toggle between play/pause icons based on game state"""
    glColor3f(1.0, 0.75, 0.0)  # Amber color
    
    x, y = play_pause_button["x"] + 20, play_pause_button["y"] + 15




    if game_state == "playing":
        
        # Pause icon: two vertical bars
        draw_line_midpoint(x - 5, y - 10, x - 5, y + 10)
        draw_line_midpoint(x + 5, y - 10, x + 5, y + 10)
        
    else:
        # Play icon: right-pointing triangle
        draw_line_midpoint(x - 8, y - 10, x + 8, y)
        draw_line_midpoint(x + 8, y, x - 8, y + 10)
        draw_line_midpoint(x - 8, y + 10, x - 8, y - 10)


def draw_exit_button():
    
    """Render exit button (X shape)"""
    glColor3f(1.0, 0.0, 0.0)  # Red color
    x, y = exit_button["x"] + 20, exit_button["y"] + 15

    # X shape: two crossing diagonals
    draw_line_midpoint(x - 10, y - 10, x + 10, y + 10)
    draw_line_midpoint(x - 10, y + 10, x + 10, y - 10)


def check_collision(
    diamond_x, diamond_y, diamond_size, catcher_x, catcher_y, catcher_width
):
    """Axis-Aligned Bounding Box collision detection"""
    # Diamond bounding box
    d_left = diamond_x - diamond_size // 2
    
    
    d_right = diamond_x + diamond_size // 2
    
    d_top = diamond_y + diamond_size // 2
    
    d_bottom = diamond_y - diamond_size // 2

    # Catcher bounding box
    c_left = catcher_x - catcher_width // 2
    
    c_right = catcher_x + catcher_width // 2
    c_top = catcher_y + 15
    
    c_bottom = catcher_y

    # AABB collision check (overlap on both axes)
    return (
        d_left < c_right and d_right > c_left and d_bottom < c_top and d_top > c_bottom
    )


def spawn_new_diamond():
    
    """Create new diamond at random position with random (bright) color"""
    global diamond_x, diamond_y, diamond_color
    
    diamond_x = random.randint(50, 450)
    
    diamond_y = 480
    # Random color, but force one channel to full so it is always bright
    diamond_color = [random.uniform(0.3, 1.0) for _ in range(3)]
    diamond_color[random.randint(0, 2)] = 1.0


def reset_game():
    
    """Reset game to initial state"""
    global game_state, score, catcher_x, diamond_speed
    game_state = "playing"
    
    score = 0
    catcher_x = 250
    
    diamond_speed = 100
    spawn_new_diamond()
    print("Starting Over")


def update_game(delta_time):
    """Update game state based on time elapsed"""
    global diamond_y, score, game_state, diamond_speed, catcher_x

    if game_state != "playing":
        return

    # Speed increases gradually with time: v = u + a*t
    diamond_speed += diamond_acceleration * delta_time

    # Update diamond position using velocity and time
    diamond_y -= diamond_speed * delta_time

    # Cheat mode: slide the catcher toward the diamond (no teleporting)
    if cheat_mode:
        # fast enough to always reach the diamond before it lands
        cheat_speed = max(catcher_speed, 2 * diamond_speed)
        step = cheat_speed * delta_time
        diff = diamond_x - catcher_x
        if abs(diff) <= step:
            catcher_x = diamond_x
        elif diff > 0:
            catcher_x += step
        else:
            catcher_x -= step
        # Keep inside the screen
        if catcher_x < catcher_width // 2:
            catcher_x = catcher_width // 2
        if catcher_x > 500 - catcher_width // 2:
            catcher_x = 500 - catcher_width // 2

    # Collision check
    if check_collision(
        diamond_x, diamond_y, diamond_size, catcher_x, 50, catcher_width
    ):
        score += 1
        print(f"Score: {score}")
        spawn_new_diamond()

    # Diamond missed (fell below catcher)
    elif diamond_y < 30:
        game_state = "game_over"
        print(f"Game Over! Final Score: {score}")


def display():
    """OpenGL render callback: draw all game elements"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw diamond (if game not over)
    if game_state != "game_over":
        draw_diamond(int(diamond_x), int(diamond_y), diamond_size, diamond_color)

    # Draw catcher (red if game over)
    draw_catcher(int(catcher_x), 50, catcher_width, game_state == "game_over")

    # Draw UI buttons
    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()

    glutSwapBuffers()


def animate():
    """Animation controller: calculates delta time and updates game"""
    global last_time

    # Calculate time since last frame
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Avoid huge jumps (e.g. when the window is dragged)
    if delta_time > 0.05:
        delta_time = 0.05

    # Update game logic
    update_game(delta_time)
    # Trigger redraw
    glutPostRedisplay()


def keyboard_listener(key, x, y):
    """Handle arrow keys (catcher movement) and the 'c' key (cheat mode)"""
    global catcher_x, cheat_mode, last_key_time

    # Time elapsed since the previous key event (delta time for key movement)
    now = time.time()
    key_dt = now - last_key_time
    last_key_time = now
    if key_dt > 0.05:
        key_dt = 0.05

    # Cheat mode toggle (normal key)
    if key == b"c" or key == b"C":
        cheat_mode = not cheat_mode
        print("Cheat Mode ON" if cheat_mode else "Cheat Mode OFF")

    # Manual movement only while playing and not in cheat mode
    elif game_state == "playing" and not cheat_mode:
        if key == GLUT_KEY_LEFT:
            catcher_x -= catcher_speed * key_dt
            # Clamp to left boundary
            if catcher_x < catcher_width // 2:
                catcher_x = catcher_width // 2
        elif key == GLUT_KEY_RIGHT:
            catcher_x += catcher_speed * key_dt
            # Clamp to right boundary
            if catcher_x > 500 - catcher_width // 2:
                catcher_x = 500 - catcher_width // 2

    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    """Handle mouse clicks on UI buttons"""
    global game_state

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert to OpenGL coordinates (origin at bottom-left)
        gl_y = 500 - y

        # Restart button click
        
        
        if (
            restart_button["x"] <= x <= restart_button["x"] + restart_button["width"]
            and restart_button["y"]
            <= gl_y
            <= restart_button["y"] + restart_button["height"]
        ):
            reset_game()
            
            
            

        # Play/Pause button click
        elif (
            
            play_pause_button["x"]
            <= x
            <= play_pause_button["x"] + play_pause_button["width"]
            and 
            play_pause_button["y"]
            <= gl_y
            <= play_pause_button["y"] + play_pause_button["height"]
        ):
            # Toggle between playing and paused states
            if game_state == "playing":
                
                game_state = "paused"
                
            elif game_state == "paused":
                
                game_state = "playing"
                

        # Exit button click
        elif (
            exit_button["x"] <= x <= exit_button["x"] + exit_button["width"]
            and exit_button["y"] <= gl_y <= exit_button["y"] + exit_button["height"]
        ):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()  # Graceful exit

    glutPostRedisplay()


def init():
    """Initialize OpenGL settings"""
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Set 2D coordinate system (500x500)
    glOrtho(0.0, 500.0, 0.0, 500.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Configure rendering
    glPointSize(2.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background


def main():
    """Game entry point: setup and start game loop"""
    global last_time, last_key_time
    last_time = time.time()  # Initialize timing
    last_key_time = time.time()

    print("Catch the Diamonds Game!")
    print("Use LEFT and RIGHT arrow keys to move the catcher")
    print("Press 'c' to toggle Cheat Mode")
    print("Click buttons to restart, pause/play, or exit")

    # GLUT initialization
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")

    init()  # OpenGL setup
    spawn_new_diamond()  # first diamond (random bright color)

    # Register callbacks
    glutDisplayFunc(display)
    glutIdleFunc(animate)  # Continuous animation
    glutKeyboardFunc(keyboard_listener)  # Normal keys ('c')
    glutSpecialFunc(keyboard_listener)  # Arrow keys
    glutMouseFunc(mouse_listener)  # Mouse clicks

    # Start game loop
    glutMainLoop()


if __name__ == "__main__":
    main()
