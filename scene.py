from model import *
import glm
import pygame as pg

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)
        self.raqueta # Guardar una referencia a la raqueta

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # floor
        n, s, interval = 10, 2, 4 
        length = 25  
        
        for y in range(-n, n, s):
            for z in range(-n, length, s):
                if y % interval == 0 and z % interval == 0:
                    add(Cube(app, pos=(-s, y, z)))
        add(Cat(app, pos=(-3, -20, 0)))

        self.raqueta = raqueta(app, pos=(0, -10, 0), scale=(0.1, 0.1, 0.1))
        add(self.raqueta)
        # moving cube
        self.moving_cube = MovingCube(app, pos=(0, 6, 8), scale=(3, 3, 3), tex_id=1)

    def update(self):
        self.moving_cube.rot.xyz = self.app.time
        self.handle_input()

    def handle_input(self):
        speed = 0.1
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.raqueta.pos[2] -= speed
        if keys[pg.K_d]:
            self.raqueta.pos[2] += speed
        self.raqueta.m_model = self.raqueta.get_model_matrix()
