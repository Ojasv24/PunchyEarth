import random
import math
import pygame
from pygame import gfxdraw
import pymunk
from convert import convert_coordinates
from earth import Earth
from astroids import Astroids
from punch import Punch
from shield import Sheld


pygame.init()
infoObject = pygame.display.Info()
screenSize = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode(screenSize)
space = pymunk.Space()
bg = pygame.image.load("space.png").convert_alpha()

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


# sheld
sheld_sprites = pygame.sprite.Group()
sheld = Sheld(space, earthPostion, 150, 60)
sheld_sprites.add(sheld)

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
earth_astroids_collision.separate = collide2

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        punch.go_to_mouse()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        sheld.moveR()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        sheld.moveL()

    screen.fill((255, 255, 255))
    # screen.blit(bg, (0, 0))

    # for obj in obj_group:
    #     obj.draw(screen)

    punch_sprites.draw(screen)
    # pygame.draw.polygon(screen, pygame.Color("yellow"), punch.vertices)
    punch_sprites.update()

    obj_group.update()

    earth_group.draw(screen)
    # sheld_sprites.draw(screen)

    gfxdraw.polygon(screen, sheld.get_vertices(), (232, 210, 9))
    for vertex in sheld.get_vertices():
        rand_color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        pygame.draw.circle(screen, rand_color,
                           (int(vertex[0]), int(vertex[1])), 2)
        # gfxdraw.pixel(screen, int(vertex[0]), int(vertex[1]), rand_color)

    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
