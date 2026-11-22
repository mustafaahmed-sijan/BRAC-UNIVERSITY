# CSE423 - Computer Graphics Lab Assignment 2
# Catch the Diamonds!
# Based on the supplied reference Python file.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Game state management
game_state = "playing"
score = 0
catcher_x = 250
catcher_width = 60
catcher_speed = 200
cheat_mode = False

# Diamond properties
diamond_x = random.randint(50, 450)
diamond_y = 480
diamond_size = 20
diamond_speed = 100
diamond_color = [random.uniform(0.45, 1.0), random.uniform(0.45, 1.0), random.uniform(0.45, 1.0)]

# Time tracking
last_time = time.time()
speed_increase_timer = 0

# UI button definitions
restart_button = {"x": 50, "y": 450, "width": 40, "height": 30}
play_pause_button = {"x": 230, "y": 450, "width": 40, "height": 30}
exit_button = {"x": 410, "y": 450, "width": 40, "height": 30}


def find_zone(x1, y1, x2, y2):
    """Find the zone of a line using its direction and slope."""
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


def convert_to_zone0(x, y, zone):
    """Convert a point from its original zone to Zone 0."""
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
    """Convert a Zone 0 point back to its original zone."""
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
    """Generate all Zone 0 pixels using the integer midpoint algorithm."""
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


def draw_line_midpoint(x1, y1, x2, y2):
    """Draw a line in any zone using the Zone 0 midpoint algorithm."""
    zone = find_zone(x1, y1, x2, y2)
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)

    if x1_z0 > x2_z0:
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0

    zone0_points = midpoint_line_zone0(x1_z0, y1_z0, x2_z0, y2_z0)

    glBegin(GL_POINTS)
    for x_z0, y_z0 in zone0_points:
        x_orig, y_orig = convert_from_zone0(x_z0, y_z0, zone)
        glVertex2f(x_orig, y_orig)
    glEnd()


def draw_diamond(x, y, size, color):
    """Draw a diamond using exactly four midpoint lines."""
    glColor3f(color[0], color[1], color[2])
    half_size = size // 2

    draw_line_midpoint(x, y + half_size, x + half_size, y)
    draw_line_midpoint(x + half_size, y, x, y - half_size)
    draw_line_midpoint(x, y - half_size, x - half_size, y)
    draw_line_midpoint(x - half_size, y, x, y + half_size)


def draw_catcher(x, y, width, is_game_over=False):
    """Draw the catcher bowl using exactly four midpoint lines."""
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


def draw_restart_button():
    """Draw the teal restart arrow using midpoint lines."""
    glColor3f(0.0, 0.85, 0.8)
    x = restart_button["x"] + 20
    y = restart_button["y"] + 15

    draw_line_midpoint(x, y, x - 15, y)
    draw_line_midpoint(x - 15, y, x - 10, y + 8)
    draw_line_midpoint(x - 15, y, x - 10, y - 8)


def draw_play_pause_button():
    """Draw the amber pause or play icon using midpoint lines."""
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


def draw_exit_button():
    """Draw the red exit cross using midpoint lines."""
    glColor3f(1.0, 0.0, 0.0)
    x = exit_button["x"] + 20
    y = exit_button["y"] + 15

    draw_line_midpoint(x - 10, y - 10, x + 10, y + 10)
    draw_line_midpoint(x - 10, y + 10, x + 10, y - 10)


def check_collision(diamond_x, diamond_y, diamond_size, catcher_x, catcher_y, catcher_width):
    """Check diamond-catcher overlap using AABB collision detection."""
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


def spawn_new_diamond():
    """Spawn one diamond at a random horizontal position and bright color."""
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(40, 460)
    diamond_y = 480
    diamond_color = [
        random.uniform(0.45, 1.0),
        random.uniform(0.45, 1.0),
        random.uniform(0.45, 1.0),
    ]


def reset_game():
    """Reset score, speed, catcher, diamond, and game mode."""
    global game_state, score, catcher_x, diamond_speed, speed_increase_timer, cheat_mode
    game_state = "playing"
    score = 0
    catcher_x = 250
    diamond_speed = 100
    speed_increase_timer = 0
    cheat_mode = False
    spawn_new_diamond()
    print("Starting Over")


def update_game(delta_time):
    """Update falling, collision, difficulty, and smooth Cheat Mode movement."""
    global diamond_y, score, game_state, diamond_speed, speed_increase_timer, catcher_x

    if game_state != "playing":
        return

    # Increase falling speed gradually with elapsed time.
    speed_increase_timer += delta_time
    diamond_speed = min(220, 100 + speed_increase_timer * 4)

    # In Cheat Mode, move the catcher smoothly toward the diamond.
    if cheat_mode:
        difference = diamond_x - catcher_x
        movement = 600 * delta_time
        if abs(difference) <= movement:
            catcher_x = diamond_x
        elif difference > 0:
            catcher_x += movement
        else:
            catcher_x -= movement

        if catcher_x < catcher_width // 2:
            catcher_x = catcher_width // 2
        elif catcher_x > 500 - catcher_width // 2:
            catcher_x = 500 - catcher_width // 2

    # Move the diamond down. In Cheat Mode, hold it near the catcher
    # briefly if the catcher is still moving into position.
    next_diamond_y = diamond_y - diamond_speed * delta_time
    if cheat_mode and next_diamond_y <= 80 and abs(diamond_x - catcher_x) > catcher_width // 2:
        diamond_y = 80
    else:
        diamond_y = next_diamond_y

    # Check whether the diamond has been caught.
    if check_collision(diamond_x, diamond_y, diamond_size, catcher_x, 50, catcher_width):
        score += 1
        print(f"Score: {score}")
        spawn_new_diamond()

    # Check whether the diamond has been missed.
    elif diamond_y < 30:
        game_state = "game_over"
        print(f"Game Over! Final Score: {score}")


def display():
    """Draw the game screen."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if game_state != "game_over":
        draw_diamond(int(diamond_x), int(diamond_y), diamond_size, diamond_color)

    draw_catcher(int(catcher_x), 50, catcher_width, game_state == "game_over")
    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()

    glutSwapBuffers()


def animate():
    """Calculate delta time and update the game continuously."""
    global last_time

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Avoid a large movement after the window has been inactive.
    if delta_time > 0.05:
        delta_time = 0.05

    update_game(delta_time)
    glutPostRedisplay()


def keyboard_listener(key, x, y):
    """Handle C for Cheat Mode and arrow keys for catcher movement."""
    global catcher_x, cheat_mode

    # Normal keyboard input: C toggles Cheat Mode.
    if key == b"c" or key == b"C":
        if game_state == "playing":
            cheat_mode = not cheat_mode
            if cheat_mode:
                print("Cheat Mode: ON")
            else:
                print("Cheat Mode: OFF")

    # Special keyboard input: left and right arrow keys.
    elif game_state == "playing" and not cheat_mode:
        if key == GLUT_KEY_LEFT:
            catcher_x -= catcher_speed * 0.016
            if catcher_x < catcher_width // 2:
                catcher_x = catcher_width // 2
        elif key == GLUT_KEY_RIGHT:
            catcher_x += catcher_speed * 0.016
            if catcher_x > 500 - catcher_width // 2:
                catcher_x = 500 - catcher_width // 2

    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    """Handle restart, pause/resume, and exit button clicks."""
    global game_state

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_y = 500 - y

        if (
            restart_button["x"] <= x <= restart_button["x"] + restart_button["width"]
            and restart_button["y"] <= gl_y <= restart_button["y"] + restart_button["height"]
        ):
            reset_game()

        elif (
            play_pause_button["x"] <= x <= play_pause_button["x"] + play_pause_button["width"]
            and play_pause_button["y"] <= gl_y <= play_pause_button["y"] + play_pause_button["height"]
        ):
            if game_state == "playing":
                game_state = "paused"
            elif game_state == "paused":
                game_state = "playing"

        elif (
            exit_button["x"] <= x <= exit_button["x"] + exit_button["width"]
            and exit_button["y"] <= gl_y <= exit_button["y"] + exit_button["height"]
        ):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

    glutPostRedisplay()


def init():
    """Initialize the 2D OpenGL coordinate system."""
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(2.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def main():
    """Initialize GLUT, register callbacks, and start the game."""
    global last_time
    last_time = time.time()

    print("Catch the Diamonds Game!")
    print("Use LEFT and RIGHT arrow keys to move the catcher")
    print("Press C to toggle Cheat Mode")
    print("Click the buttons to restart, pause/play, or exit")

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")

    init()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(keyboard_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


if __name__ == "__main__":
    main()
