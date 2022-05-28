from turtle import pu
import pygame

from punch import Punch

pygame.init()


screen = pygame.display.set_mode((1280, 720))

# Punch

punch_sprites = pygame.sprite.Group()
punch = Punch(640, 350)
punch_sprites.add(punch)


exit = False
clock = pygame.time.Clock()
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        
        punch.angle()
            
    screen.fill((29, 17, 53))
    punch_sprites.draw(screen)
    punch_sprites.update(640, 350)
    pygame.display.flip()
    clock.tick(60)
