from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

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
                        #AD-AT,AR-AB,R-L
        add(Cat(app, pos=(-3, -20, 0)))
        
        # moving cube
        self.moving_cube = MovingCube(app, pos=(0, 6, 8), scale=(3, 3, 3), tex_id=1)
        

    def update(self):
        self.moving_cube.rot.xyz = self.app.time
