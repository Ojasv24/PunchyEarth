import random
import math
import pygame
import pymunk
from convert import convert_coordinates
from earth import Earth
from astroids import Astroids
from punch import Punch


pygame.init()
screenSize = (1920, 1080)
screen = pygame.display.set_mode(screenSize)
space = pymunk.Space()

# variables

earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
earthGravityForce = 0.002
earthSize = (200, 200)

punchSize = (50, 90)


# earth
earth_group = pygame.sprite.Group()
earth = Earth(space, earthPostion, earthSize, 1)
earth_group.add(earth)

# astroids
obj_group = pygame.sprite.Group()
for i in range(10):
    rand_color = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    obj = Astroids(space, (random.randint(0, 1200), random.randint(
        0, 700)), earthPostion, earthGravityForce, rand_color)
    obj_group.add(obj)


# punch
punch_sprites = pygame.sprite.Group()
punch = Punch(space, punchSize, earthPostion, 1)
punch_sprites.add(punch)

exit = False
clock = pygame.time.Clock()


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def collide(arbiter, space, data):
    # print('hi')
    punch.returnBack()
    return True


def collide2(arbiter, space, data):
    # arbiter.shapes[1].body.position = 0, 0
    # space.remove(arbiter.shapes[1], arbiter.shapes[1].body)
    # print(arbiter.shapes[1].body)
    # print('help')
    return True


punch_astroids_collision = space.add_collision_handler(1, 2)
punch_astroids_collision.begin = collide

earth_astroids_collision = space.add_collision_handler(3, 2)
earth_astroids_collision.begin = collide2

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        punch.go_to_mouse()

    screen.fill((29, 17, 53))

    for obj in obj_group:
        obj.draw(screen)

    # print(punch.shape.bb.top)
    # bb = punch.shape.bb
    # print(punch.vertices)

    punch_sprites.draw(screen)
    # pygame.draw.polygon(screen, pygame.Color("yellow"), punch.vertices)
    punch_sprites.update()

    obj_group.update()

    earth_group.draw(screen)
    # pygame.draw.circle(screen, pygame.Color("yellow"),
    #                    earth.body.position, earth.shape.radius)

    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
