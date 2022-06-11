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
        self.shieldDestroyed = False
        self.space = pymunk.Space()

    def setup(self):
        self.space = pymunk.Space()
        add_collision_handler(self.space, (PUNCH, asteroid),
                              lambda *_: self.punch.returnBackAfterClick(
                                  self.clock_time),
                              lambda *_: pygame.mixer.Channel(1).play(pygame.mixer.Sound('./assets/punch_cut.mp3')))

        add_collision_handler(self.space, (EARTH, asteroid),
                              lambda *_: self.earth_asteroid_collsion_begin(
                                  *_),
                              lambda arbiter, space, data: self.earth.reduce_health(max(arbiter.shapes[1].body.kinetic_energy / 100, 10)))

        add_collision_handler(self.space, (SHEILD, asteroid),
                              lambda *_: self.shield_astorid_collision_begin(
                                  *_),
                              lambda arbiter, space, data: self.shield.reduce_health(max(arbiter.shapes[1].body.kinetic_energy / 10000, 20)))

        self.earth_group = pygame.sprite.Group()
        self.earth = Earth(self.space, self.earthPostion, self.earthSize, 1)
        self.earth_group.add(self.earth)

        # asteroids
        self.asteroid_group = pygame.sprite.Group()
        self.last_spawn_time = time.time()

        # punch
        self.punch_group = pygame.sprite.Group()
        self.punch = Punch(self.space, self.punchSize, self.earthPostion, 1)
        self.punch_group.add(self.punch)

        # shield
        self.shield_group = pygame.sprite.Group()
        self.shield = shield(self.space, self.earthPostion, 130, 60)
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

        if self.shield.health <= 0 and not self.shieldDestroyed:
            self.destroyshield()
            self.shieldDestroyed = True
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
        self.clock_time.start = time.time()
        body: pymunk.Body = arbiter.shapes[1].body
        if arbiter.is_first_contact:
            body.velocity = arbiter.normal * 1000

    def get_random_position(self):
        screenX, screenY = self.screenSize
        x = random.choice([random.randint(-screenX, 0), random
                          .randint(screenX, 2*screenX)])
        y = random.choice([random.randint(-screenY, 0), random
                          .randint(screenY, 2*screenY)])
        return x, y

    def genrateasteroids(self):
        now = time.time()
        if len(self.asteroid_group) >= self.asteroidNumber or (now - self.last_spawn_time) < 3:
            return

        colors = [(218, 165, 32),	(255, 69, 0), (124, 252, 0), (127, 255, 212), (255, 0, 255),
                  (255, 228, 196), (0, 191, 255), (250, 128, 114), (224, 255, 255),
                  (244, 164, 96), (255, 228, 225),	(240, 255, 255),	(255, 255, 255),
                  (255, 255, 0), (144, 238, 144),	(0, 250, 154), (175, 238, 238),
                  (147, 112, 219),	(221, 160, 221),	(216, 191, 216),	(255, 192, 203),
                  (0, 191, 255),	(135, 206, 250),	(245, 255, 250), (211, 211, 211)]
        # print(len(colors))
        # rand_color = (random.randint(0, 255), random.randint(
        #     0, 255), random.randint(0, 255))

        pos = self.get_random_position()
        asteroid = asteroids(self.space, pos, self.earthPostion,
                             self.earthGravityForce, random.choice(colors))
        self.asteroid_group.add(asteroid)
        self.last_spawn_time = now
