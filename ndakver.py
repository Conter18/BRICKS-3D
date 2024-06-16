import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("BRICKS 3D")

# Configuración de OpenGL
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -10)

# Vértices y superficies del cubo
cube_vertices = [
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
]

cube_surfaces = [
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
]

cube_tex_coords = [
    (0, 0), (1, 0), (1, 1), (0, 1)
]

# Pala
paddle_position = [0, -3.5, 0]
paddle_size = [2, 0.2, 0.5]

# Cargar Textura de la pala
def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    
    return texture_id

texture_id = load_texture('textures/metalpala.png')

# Función para dibujar un cubo con textura
def draw_cube(size, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for surface in cube_surfaces:
        for i, vertex in enumerate(surface):
            glTexCoord2fv(cube_tex_coords[i])
            glVertex3f(cube_vertices[vertex][0] * size[0],
                       cube_vertices[vertex][1] * size[1],
                       cube_vertices[vertex][2] * size[2])
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

def draw_paddle():
    glPushMatrix()
    glTranslatef(*paddle_position)
    draw_cube(paddle_size, texture_id)
    glPopMatrix()

# Configuración inicial de OpenGL para texturas
glEnable(GL_TEXTURE_2D)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de la pala
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_position[0] > -WIDTH / 200:
        paddle_position[0] -= 0.05
    if keys[pygame.K_RIGHT] and paddle_position[0] < WIDTH / 200:
        paddle_position[0] += 0.05

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar la pala
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10)
    draw_paddle()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
