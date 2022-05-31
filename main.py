from lib2to3.pytree import convert
import pygame
import pymunk
from convert import convert_coordinates
from objects import objects
from punch import Punch

pygame.init()

screen = pygame.display.set_mode((1280, 720))
space = pymunk.Space()


# Punch
punch_sprites = pygame.sprite.Group()
punch = Punch(640, 350, space)
punch_sprites.add(punch)

obj_group = pygame.sprite.Group()
obj = objects(300, 300, space)
# obj1 = objects(400, 300, space)
obj_group.add(obj)
# obj_group.add(obj1)
exit = False
clock = pygame.time.Clock()


def collide(arbiter, space, data):
    print('hello')
    return True


handler = space.add_collision_handler(1, 2)
handler.post_solve = collide
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:

        punch.angle()

    screen.fill((29, 17, 53))
    punch_sprites.draw(screen)
    obj_group.draw(screen)
    # print(punch.shape.bb.top)
    bb = punch.shape.bb
    pygame.draw.polygon(screen, (0, 255, 0),
                        [convert_coordinates((bb.left, bb.top)), convert_coordinates((bb.left, bb.bottom)), convert_coordinates((bb.right, bb.bottom)), convert_coordinates((bb.right, bb.top))], 10)

    pygame.draw.circle(screen, (0, 255, 0),
                       convert_coordinates(obj.body.position), 50)

    punch_sprites.update(640, 350)
    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
