import copy
import random
import time
import pygame
import pymunk
from astroids import Astroids
from clock import Clock
from collision_handler import ASTROID, EARTH, PUNCH, SHEILD, add_collision_handler
from earth import Earth
from punch import Punch
from setup import Game
from shield import Sheld

from startGame import game


pygame.init()
pygame.mixer.init()

infoObject = pygame.display.Info()
screenSize = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode(screenSize)

bg = pygame.image.load("./assets/space.png").convert_alpha()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./assets/bg_music.mp3'), -1)
pygame.mixer.music.set_volume(0.3)

page = 'startscreen'


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):

        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y -
                             2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                         self.width, self.height), 0, 2, 3)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


startButton = Button(
    (0, 0, 255), screenSize[0] / 2 - 100, screenSize[1] / 2 - 50, 100, 50, 'Start')
retry = Button(
    (0, 0, 255), screenSize[0] / 2 - 100, screenSize[1] / 2 - 50, 100, 50, 'Retry')

infoObject = pygame.display.Info()
# variables
earthPostion = (screenSize[0] / 2, screenSize[1] / 2)
earthGravityForce = 0.002
earthSize = (200, 200)

punchSize = (50, 90)


exit = False
clock = pygame.time.Clock()

game = Game(screenSize, earthGravityForce, earthSize, punchSize)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if page == 'startscreen' and screenSize[0] / 2 - 100 < mouse[0] < screenSize[0] / 2 and screenSize[1] / 2 - 50 < mouse[1] < screenSize[1] / 2:
                game.setup()
                page = 'game'
            if page == 'end' and screenSize[0] / 2 - 100 < mouse[0] < screenSize[0] / 2 and screenSize[1] / 2 - 50 < mouse[1] < screenSize[1] / 2:
                game.setup()
                page = 'game'

    screen.fill((29, 17, 53))
    screen.blit(bg, (0, 0))
    mouse = pygame.mouse.get_pos()

    if page == 'startscreen':
        startButton.draw(screen)
    if page == 'game':
        game.render(screen)
        if game.earth.health <= 0:
            page = 'end'
    if page == 'end':
        retry.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    game.space.step(1/60)
