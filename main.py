import pygame
from setup import Game
from pages import Page

pygame.init()
pygame.mixer.init()

infoObject = pygame.display.Info()
screenSize = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)

bg = pygame.image.load("./assets/space.png").convert_alpha()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./assets/bg_music.mp3'), -1)
pygame.mixer.music.set_volume(0.3)

page = 'start'

infoObject = pygame.display.Info()
# variables
earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
earthGravityForce = 0.006
earthSize = (200, 200)
punchSize = (50, 90)
asteroidNumber = 20

exit = False
clock = pygame.time.Clock()

game = Game(screenSize, earthGravityForce,
            earthSize, punchSize, asteroidNumber)
page_look = Page(screenSize)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if page == 'start' and page_look.startButton.x < mouse[0] < page_look.startButton.x + page_look.startButton.width and page_look.startButton.y < mouse[1] < page_look.startButton.y + page_look.startButton.height:
                game.setup()
                page = 'game'
            if (page == 'start' or page == 'endLose' or page == 'endWin') and page_look.quitButton.x < mouse[0] < page_look.quitButton.x + page_look.quitButton.width and page_look.quitButton.y < mouse[1] < page_look.quitButton.y + page_look.quitButton.height:
                exit = True
            if (page == 'endLose' or page == 'endWin') and page_look.retry.x < mouse[0] < page_look.retry.x + page_look.retry.width and page_look.retry.y < mouse[1] < page_look.retry.y + page_look.retry.height:
                game.setup()
                page = 'game'

    screen.fill((29, 17, 53))
    screen.blit(bg, (0, 0))
    mouse = pygame.mouse.get_pos()

    if page == 'start':
        page_look.startPage(screen)
    if page == 'game':
        game.render(screen)
        if game.earth.health <= 0:
            page = 'endLose'
        if game.clock_time.time <= 0:
            page = 'endWin'

    if page == 'endLose':
        page_look.endPage(screen)
    if page == 'endWin':
        page_look.winPage(screen)

    pygame.display.flip()
    clock.tick(60)
    game.space.step(1/60)
