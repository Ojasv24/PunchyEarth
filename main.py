from lib2to3.pytree import convert
import pygame
import pymunk
from convert import convert_coordinates
from earth import Earth
from objects import objects

from punch import Punch

pygame.init()

screen = pygame.display.set_mode((1280, 720))
space = pymunk.Space()

#earth
earth_group = pygame.sprite.Group()
earth = Earth()
earth_group.add(earth)


obj_group = pygame.sprite.Group()
obj = objects(0, 0, space)
# obj1 = objects(400, 300, space)
obj_group.add(obj)
# obj_group.add(obj1)


# test
punch_sprites = pygame.sprite.Group()
test = Punch(space)
punch_sprites.add(test)

exit = False
clock = pygame.time.Clock()


def collide(arbiter, space, data):
    print('hellp')
    test.returnBack()


handler = space.add_collision_handler(1, 2)
handler.separate = collide
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        test.cal_angel()

    screen.fill((29, 17, 53))
    punch_sprites.draw(screen)
    
    # obj_group.draw(screen)
    # print(punch.shape.bb.top)
    # bb = punch.shape.bb
    # print(punch.vertices)
    # pygame.draw.polygon(screen, pygame.Color("yellow"), test.vertices)
    punch_sprites.update()

    pygame.draw.circle(screen, (0, 255, 0),
                       obj.body.position, 30)

    earth_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    space.step(1/60)
