import math
import time
from pygame import gfxdraw
import random
import pygame
import pymunk
from asteroid import asteroids
from clock import Clock
from collision_handler import asteroid, EARTH, PUNCH, SHEILD, add_collision_handler

from earth import Earth
from punch import Punch
from shield import shield


class Game():
    def __init__(self, screenSize, earthGravityForce, earthSize, punchSize, asteroidNumber) -> None:
        self.screenSize = screenSize
        self.earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
        self.earthGravityForce = earthGravityForce
        self.earthSize = earthSize
        self.punchSize = punchSize
        self.asteroidNumber = asteroidNumber
        self.space = pymunk.Space()

    def setup(self):
        self.space = pymunk.Space()
        add_collision_handler(self.space, (PUNCH, asteroid),
                              lambda *_: self.punch.returnBackAfterClick(
                                  self.clock_time),
                              lambda *_: pygame.mixer.Channel(1).play(pygame.mixer.Sound('./assets/punch_cut.mp3')))

        add_collision_handler(self.space, (EARTH, asteroid),
                              lambda *_: self.earth_asteroid_collsion_begin(*_),
                              lambda arbiter, space, data: self.earth.reduce_health(arbiter.shapes[1].body.kinetic_energy / 100))

        add_collision_handler(self.space, (SHEILD, asteroid),
                              lambda *_: self.shield_astorid_collision_begin(
                                  *_),
                              lambda arbiter, space, data: self.shield.reduce_health(arbiter.shapes[1].body.kinetic_energy / 1000))

        self.earth_group = pygame.sprite.Group()
        self.earth = Earth(self.space, self.earthPostion, self.earthSize, 1)
        self.earth_group.add(self.earth)

        # asteroids
        self.asteroid_group = pygame.sprite.Group()
        self.genrateasteroids()

        # punch
        self.punch_group = pygame.sprite.Group()
        self.punch = Punch(self.space, self.punchSize, self.earthPostion, 1)
        self.punch_group.add(self.punch)

        # shield
        self.shield_group = pygame.sprite.Group()
        self.shield = shield(self.space, self.earthPostion, 150, 60)
        self.shield_group.add(self.shield)

        # clock
        self.clock_group = pygame.sprite.Group()
        self.clock_time = Clock((self.screenSize[0] - 100, 50))
        self.clock_group.add(self.clock_time)

    def render(self, screen):
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0]:
            self.punch.go_to_mouse()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.shield.moveR()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.shield.moveL()
        [asteroid.draw(screen, self.space) for asteroid in self.asteroid_group]

        if len(self.asteroid_group) < self.asteroidNumber:
            self.genrateasteroids()

        self.punch_group.draw(screen)
        self.punch_group.update()

        self.asteroid_group.update()
        self.asteroid_group.draw(screen)

        self.earth_group.draw(screen)
        self.earth.drawHealthBar(screen)

        self.shield.drawHealthBar(screen)
        self.clock_group.draw(screen)
        self.clock_time.drawTime(screen)

        self.shield.draw(screen)

    def earth_asteroid_collsion_begin(self, arbiter, space, data):
        self.clock_time.start = time.time()
        elem = next(filter(lambda o: o.body ==
                    arbiter.shapes[1].body, self.asteroid_group))
        self.asteroid_group.remove(elem)
        space.remove(arbiter.shapes[1], arbiter.shapes[1].body)

    def destroyshield(self):
        self.space.remove(self.shield.shape, self.shield.body)

    def shield_astorid_collision_begin(self, arbiter: pymunk.Arbiter, space, data):
        if self.shield.health <= 0:
            self.destroyshield()
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

    def genrateasteroids(self):
        for i in range(self.asteroidNumber - len(self.asteroid_group)):
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            asteroid = asteroids(self.space, (random.randint(-1200, 2400), random.randint(
                -700, 1400)), self.earthPostion, self.earthGravityForce, rand_color)
            self.asteroid_group.add(asteroid)
