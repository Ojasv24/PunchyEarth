import pygame

pygame.init()


screen = pygame.display.set_mode((1280,720))

exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill()    

