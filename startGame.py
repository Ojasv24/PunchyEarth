import random
import time
import pygame
from pygame import gfxdraw
import pymunk
from clock import Clock
from collision_handler import ASTROID, EARTH, PUNCH, SHEILD, add_collision_handler
from earth import Earth
from astroids import Astroids
from punch import Punch
from shield import Sheld


def game(screenSize, screen, space, punch, sheld, obj_group, earthPostion, earthGravityForce, punch_sprites, earth_group, earth, clock_group, clock_time, page):
    print(earth.health)
    if earth.health <= 0:
        page = 'end'

    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        punch.go_to_mouse()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        sheld.moveR()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        sheld.moveL()

    [obj.draw(screen, space) for obj in obj_group]

    if len(obj_group) < 10:
        for i in range(10 - len(obj_group)):
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            obj = Astroids(space, (random.randint(0, 1200), random.randint(
                0, 700)), earthPostion, earthGravityForce, rand_color)
            obj_group.add(obj)

    punch_sprites.draw(screen)
    punch_sprites.update()

    obj_group.update()

    earth_group.draw(screen)
    earth.drawHealthBar(screen)
    # pygame.draw.circle(screen, (0, 0, 255),
    #                    earth.body.position, earth.shape.radius)
    screen.get_height()
    screen.get_width()
    # sheld_sprites.draw(screen)
    sheld.drawHealthBar(screen)
    clock_group.draw(screen)
    clock_time.drawTime(screen)

    gfxdraw.filled_polygon(screen, sheld.get_vertices(), (232, 210, 9))
