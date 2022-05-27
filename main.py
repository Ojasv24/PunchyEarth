import pygame

from punch import Punch

pygame.init()


screen = pygame.display.set_mode((1280, 720))

# Punch

punch_sprites = pygame.sprite.Group()
punch = Punch(20, 20)
punch_sprites.add(punch)


exit = False
clock = pygame.time.Clock()
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    screen.fill((29, 17, 53))
    punch_sprites.draw(screen)
    punch_sprites.update(650,355)
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(punch.rect.midtop[0], punch.rect.midtop[1], 60, 60))
    pygame.display.flip()
    clock.tick(60)
