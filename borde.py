import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Tamaño del marco
BOX_SIZE = 10.0

# Variables para la pelota
ballRadius = 1.0
ballPos = np.array([0.0, 0.0, 0.0])
ballSpeed = np.array([0.02, 0.02, 0.02])

def draw_box(size):
    glBegin(GL_LINES)
    for x in (-size, size):
        for y in (-size, size):
            for z in (-size, size):
                glVertex3f(x, y, z)
                glVertex3f(-x, y, z)
                glVertex3f(x, -y, z)
                glVertex3f(x, y, -z)
    glEnd()

def draw_sphere(radius, slices, stacks):
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        
        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j) / slices
            x = np.cos(lng)
            y = np.sin(lng)
            
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()

def draw_ball():
    glPushMatrix()
    glTranslatef(*ballPos)
    draw_sphere(ballRadius, 20, 20)
    glPopMatrix()

def update_ball_position():
    global ballPos, ballSpeed
    ballPos += ballSpeed

    # Verificar colisiones con el marco y revertir la velocidad si es necesario
    for i in range(3):
        if abs(ballPos[i]) + ballRadius > BOX_SIZE:
            ballSpeed[i] = -ballSpeed[i]
            ballPos[i] = np.sign(ballPos[i]) * (BOX_SIZE - ballRadius)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_box(BOX_SIZE)
        draw_ball()
        update_ball_position()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
