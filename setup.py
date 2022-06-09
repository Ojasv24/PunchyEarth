import math
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
    def __init__(self, screenSize, earthGravityForce, earthSize, punchSize, astroidNumber) -> None:
        self.screenSize = screenSize
        self.earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
        self.earthGravityForce = earthGravityForce
        self.earthSize = earthSize
        self.punchSize = punchSize
        self.astroidNumber = astroidNumber
        self.space = pymunk.Space()

    def setup(self):
        self.space = pymunk.Space()
        add_collision_handler(self.space, (PUNCH, ASTROID),
                              lambda *_: self.punch.returnBackAfterClick(
                                  self.clock_time),
                              lambda *_: pygame.mixer.Channel(1).play(pygame.mixer.Sound('./assets/punch_cut.mp3')))

        add_collision_handler(self.space, (EARTH, ASTROID),
                              lambda *_: self.earth_astroid_collsion_begin(*_),
                              lambda arbiter, space, data: self.earth.reduce_health(arbiter.shapes[1].body.kinetic_energy / 100))

        add_collision_handler(self.space, (SHEILD, ASTROID),
                              lambda *_: self.sheld_astorid_collision_begin(
                                  *_),
                              lambda arbiter, space, data: self.sheld.reduce_health(arbiter.shapes[1].body.kinetic_energy / 1000))

        self.earth_group = pygame.sprite.Group()
        self.earth = Earth(self.space, self.earthPostion, self.earthSize, 1)
        self.earth_group.add(self.earth)

        # astroids
        self.astroid_group = pygame.sprite.Group()
        self.genrateAstroids()
        # for i in range(10):
        # rand_color = (random.randint(0, 255), random.randint(
        #     0, 255), random.randint(0, 255))
        # obj = Astroids(self.space, (random.randint(-1200, 2400), random.randint(
        #     -700, 1400)), self.earthPostion, self.earthGravityForce, rand_color)
        # self.obj_group.add(obj)

        # punch
        self.punch_group = pygame.sprite.Group()
        self.punch = Punch(self.space, self.punchSize, self.earthPostion, 1)
        self.punch_group.add(self.punch)

        # sheld
        self.sheld_group = pygame.sprite.Group()
        self.sheld = Sheld(self.space, self.earthPostion, 150, 60)
        self.sheld_group.add(self.sheld)

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
        [astroid.draw(screen, self.space) for astroid in self.astroid_group]

        if len(self.astroid_group) < self.astroidNumber:
            self.genrateAstroids()
            # for i in range(10 - len(self.obj_group)):
            #     rand_color = (random.randint(0, 255), random.randint(
            #         0, 255), random.randint(0, 255))
            #     obj = Astroids(self.space, (random.randint(0, 1200), random.randint(
            #         0, 700)), self.earthPostion, self.earthGravityForce, rand_color)
            #     self.obj_group.add(obj)

        self.punch_group.draw(screen)
        self.punch_group.update()

        self.astroid_group.update()
        self.astroid_group.draw(screen)

        self.earth_group.draw(screen)
        self.earth.drawHealthBar(screen)
        # pygame.draw.circle(screen, (0, 0, 255),
        #                    earth.body.position, earth.shape.radius)

        # sheld_sprites.draw(screen)
        self.sheld.drawHealthBar(screen)
        self.clock_group.draw(screen)
        self.clock_time.drawTime(screen)

        self.sheld.draw(screen)

    def earth_astroid_collsion_begin(self, arbiter, space, data):
        self.clock_time.start = time.time()
        elem = next(filter(lambda o: o.body ==
                    arbiter.shapes[1].body, self.astroid_group))
        self.astroid_group.remove(elem)
        space.remove(arbiter.shapes[1], arbiter.shapes[1].body)

    def destroySheld(self):
        self.space.remove(self.sheld.shape, self.sheld.body)

    def sheld_astorid_collision_begin(self, arbiter: pymunk.Arbiter, space, data):
        if self.sheld.health <= 0:
            self.destroySheld()
        self.clock_time.start = time.time()
        sheild: pymunk.Body = arbiter.shapes[0].body
        body: pymunk.Body = arbiter.shapes[1].body
        vx, vy = body.velocity
        nx, ny = arbiter.normal
        sx, sy = sheild.position
        bx, by = body.position
        nx, ny = bx - sx, by - sy
        # print(nx, ny)
        if arbiter.is_first_contact:
            # body.velocity = 1000 * arbiter.normal
            body.apply_impulse_at_world_point(
                (math.copysign(0.1, nx), math.copysign(0.1, ny)), (0, 0))

    def genrateAstroids(self):
        for i in range(self.astroidNumber - len(self.astroid_group)):
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            astroid = Astroids(self.space, (random.randint(-1200, 2400), random.randint(
                -700, 1400)), self.earthPostion, self.earthGravityForce, rand_color)
            self.astroid_group.add(astroid)
