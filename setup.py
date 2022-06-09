import time
from pygame import gfxdraw
import random
import pygame
import pymunk
from astroids import Astroids
from clock import Clock
from collision_handler import ASTROID, EARTH, PUNCH, SHEILD, add_collision_handler

from earth import Earth
from punch import Punch
from shield import Sheld




class Game():
    def __init__(self, screenSize, earthGravityForce, earthSize, punchSize) -> None:
        self.screenSize = screenSize
        self.earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
        self.earthGravityForce = earthGravityForce
        self.earthSize = earthSize
        self.punchSize = punchSize
        self.space = pymunk.Space()

    def setup(self):
        self.space = pymunk.Space()
        add_collision_handler(self.space, (PUNCH, ASTROID), 
                        lambda *_: self.punch.returnBackAfterClick(self.clock_time),
                        lambda *_: pygame.mixer.Channel(1).play(pygame.mixer.Sound('./assets/punch_cut.mp3')))

        add_collision_handler(self.space, (EARTH, ASTROID), 
                        lambda *_: self.earth_astroid_collsion_begin(*_),
                        lambda arbiter, space, data: self.earth.reduce_health(arbiter.shapes[1].body.kinetic_energy / 10))

        add_collision_handler(self.space, (SHEILD, ASTROID), 
                        lambda *_: self.sheld_astorid_collision_begin(*_),
                        lambda arbiter, space, data: self.sheld.reduce_health(arbiter.shapes[1].body.kinetic_energy / 50))
        
        self.earth_group = pygame.sprite.Group()
        self.earth = Earth(self.space, self.earthPostion, self.earthSize, 1)
        self.earth_group.add(self.earth)

        # astroids
        self.obj_group = pygame.sprite.Group()
        for i in range(10):
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            obj = Astroids(self.space, (random.randint(0, 1200), random.randint(
                0, 700)), self.earthPostion, self.earthGravityForce, rand_color)
            self.obj_group.add(obj)

        # punch
        self.punch_sprites = pygame.sprite.Group()
        self.punch = Punch(self.space, self.punchSize, self.earthPostion, 1)
        self.punch_sprites.add(self.punch)

        # sheld
        self.sheld_sprites = pygame.sprite.Group()
        self.sheld = Sheld(self.space, self.earthPostion, 150, 60)
        self.sheld_sprites.add(self.sheld)

        # clock
        self.clock_group = pygame.sprite.Group()
        self.clock_time = Clock((self.screenSize[1] - 100, 50))
        self.clock_group.add(self.clock_time)

    def render(self, screen):
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0]:
            self.punch.go_to_mouse()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.sheld.moveR()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.sheld.moveL()
        [obj.draw(screen, self.space) for obj in self.obj_group]

        if len(self.obj_group) < 10:
            for i in range(10 - len(self.obj_group)):
                rand_color = (random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255))
                obj = Astroids(self.space, (random.randint(0, 1200), random.randint(
                    0, 700)), self.earthPostion, self.earthGravityForce, rand_color)
                self.obj_group.add(obj)

        self.punch_sprites.draw(screen)
        self.punch_sprites.update()

        self.obj_group.update()
        self.obj_group.draw(screen)

        self.earth_group.draw(screen)
        self.earth.drawHealthBar(screen)
        # pygame.draw.circle(screen, (0, 0, 255),
        #                    earth.body.position, earth.shape.radius)
        screen.get_height()
        screen.get_width()
        # sheld_sprites.draw(screen)
        self.sheld.drawHealthBar(screen)
        self.clock_group.draw(screen)
        self.clock_time.drawTime(screen)


        gfxdraw.filled_polygon(screen, self.sheld.get_vertices(), (232, 210, 9))

    def earth_astroid_collsion_begin(self,arbiter, space, data):
        self.clock_time.start = time.time()
        elem = next(filter(lambda o: o.body == arbiter.shapes[1].body, self.obj_group))
        self.obj_group.remove(elem)
        space.remove(arbiter.shapes[1], arbiter.shapes[1].body)

    def sheld_astorid_collision_begin(self,arbiter: pymunk.Arbiter, space, data):
        self.clock_time.start = time.time()
        # sheild: pymunk.Body = arbiter.shapes[0].body
        # body: pymunk.Body = arbiter.shapes[1].body
        # vx, vy = body.velocity
        # nx, ny = arbiter.normal
        # sx, sy = sheild.position
        # bx, by = body.position
        # nx, ny = bx - sx , by - sy
        # # print(nx, ny)
        # if arbiter.is_first_contact:
        #     # body.velocity = 1000 * arbiter.normal
        #     body.apply_impulse_at_world_point((math.copysign(0.1, nx), math.copysign(0.1, ny)), (0, 0))

    
    