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


pygame.init()
pygame.mixer.init()

infoObject = pygame.display.Info()
screenSize = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode(screenSize)
space = pymunk.Space()
bg = pygame.image.load("./assets/space.png").convert_alpha()
pygame.mixer.music.load("./assets/bg_music.mp3")
pygame.mixer.music.load("./assets/punch_cut.mp3")
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./assets/bg_music.mp3'))
pygame.mixer.music.set_volume(0.3)
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


# clock
clock_group = pygame.sprite.Group()
clock_time = Clock((infoObject.current_w - 100, 50))
clock_group.add(clock_time)

exit = False
clock = pygame.time.Clock()

# collsion


def earth_astroid_collsion_begin(arbiter, space, data):
    clock_time.start = time.time()
    elem = next(filter(lambda o: o.body == arbiter.shapes[1].body, obj_group))
    obj_group.remove(elem)
    space.remove(arbiter.shapes[1], arbiter.shapes[1].body)

def sheld_astorid_collision_begin(arbiter: pymunk.Arbiter, space, data):
    clock_time.start = time.time()
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

add_collision_handler(space, (PUNCH, ASTROID), 
                      lambda *_: punch.returnBackAfterClick(clock_time),
                      lambda *_: pygame.mixer.Channel(1).play(pygame.mixer.Sound('./assets/punch_cut.mp3')))

add_collision_handler(space, (EARTH, ASTROID), 
                      lambda *_: earth_astroid_collsion_begin(*_),
                      lambda arbiter, space, data: earth.reduce_health(arbiter.shapes[1].body.kinetic_energy / 10))

add_collision_handler(space, (SHEILD, ASTROID), 
                      lambda *_: sheld_astorid_collision_begin(*_),
                      lambda arbiter, space, data: sheld.reduce_health(arbiter.shapes[1].body.kinetic_energy / 50))

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

    screen.fill((29, 17, 53))
    screen.blit(bg, (0, 0))

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

    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
