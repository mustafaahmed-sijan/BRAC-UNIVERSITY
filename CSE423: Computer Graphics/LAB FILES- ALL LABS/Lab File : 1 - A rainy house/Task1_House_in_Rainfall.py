from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

W_Width, W_Height = 500, 500

brightness = 0.0   # 0 = night (black sky), 1 = day (light blue sky)
rain_shift = 0.0   # how much the rain is bent (negative = left, positive = right)
rain_drops = []


class RainDrop:
    def __init__(self):
        self.x = random.randint(-250, 250)
        self.y = random.randint(-20, 250)
        self.speed = random.randint(3, 6)


def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()


def draw_rectangle(x1, y1, x2, y2):
    # a rectangle made from two triangles
    draw_triangle(x1, y1, x2, y1, x2, y2)
    draw_triangle(x1, y1, x2, y2, x1, y2)


def draw_ground():
    glColor3f(0.5, 0.35, 0.1)
    draw_rectangle(-250, -250, 250, -20)


def draw_trees():
    glColor3f(0.0, 0.7, 0.0)
    for x in range(-240, 250, 40):
        if -110 < x < 110:      # leave space for the house
            continue
        draw_triangle(x - 20, -20, x + 20, -20, x, 30)


def draw_house():
    # walls
    glColor3f(1.0, 1.0, 0.8)
    draw_rectangle(-90, -20, 90, 70)

    # roof
    glColor3f(0.4, 0.3, 0.7)
    draw_triangle(-100, 70, 100, 70, 0, 130)

    # door
    glColor3f(0.2, 0.5, 0.9)
    draw_rectangle(-15, -20, 15, 35)

    # windows
    glColor3f(0.3, 0.6, 0.9)
    draw_rectangle(-70, 10, -35, 45)
    draw_rectangle(35, 10, 70, 45)

    # window crosses
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(-52, 10)
    glVertex2f(-52, 45)
    glVertex2f(-70, 28)
    glVertex2f(-35, 28)
    glVertex2f(52, 10)
    glVertex2f(52, 45)
    glVertex2f(35, 28)
    glVertex2f(70, 28)
    glEnd()


def draw_rain():
    glColor3f(0.4, 0.5, 1.0)
    glLineWidth(1)
    glBegin(GL_LINES)
    for d in rain_drops:
        glVertex2f(d.x, d.y)
        glVertex2f(d.x + rain_shift, d.y - 15)
    glEnd()


def keyboardListener(key, x, y):
    global brightness
    if key == b'd':
        brightness = round(min(1.0, brightness + 0.1), 1)
        print("Brightness:", brightness)
    if key == b'n':
        brightness = round(max(0.0, brightness - 0.1), 1)
        print("Brightness:", brightness)
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global rain_shift
    if key == GLUT_KEY_LEFT:
        rain_shift = max(-20, rain_shift - 2)
        print("Rain shift:", rain_shift)
    if key == GLUT_KEY_RIGHT:
        rain_shift = min(20, rain_shift + 2)
        print("Rain shift:", rain_shift)
    glutPostRedisplay()


def display():
    glClearColor(brightness * 0.53, brightness * 0.81, brightness * 0.92, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    draw_ground()
    draw_trees()
    draw_house()
    draw_rain()

    glutSwapBuffers()


def animate():
    for d in rain_drops:
        d.y -= d.speed
        d.x += rain_shift * 0.1

        if d.y < -20:           # reached the ground, start again from the top
            d.y = 250
            d.x = random.randint(-250, 250)
        if d.x > 250:
            d.x = -250
        if d.x < -250:
            d.x = 250
    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)
    for i in range(200):
        rain_drops.append(RainDrop())


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Task 1: House in Rainfall")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()
