import pygame
import math


class Punch(pygame.sprite.Sprite):
    SPEED = 10

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('1.png'))
        self.sprites.append(pygame.image.load('2.png'))
        self.sprites.append(pygame.image.load('3.png'))
        self.sprites.append(pygame.image.load('4.png'))
        self.sprites.append(pygame.image.load('5.png'))
        self.sprites.append(pygame.image.load('6.png'))

        self.x = pos_x
        self.y = pos_y
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, pos_x, pos_y):
        # animation
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        mouse_pos = pygame.mouse.get_pos()
        mouse_posX = mouse_pos[0]
        mouse_posY = mouse_pos[1]
        mouse_posX = mouse_posX - self.rect.centerx
        mouse_posY = mouse_posY - self.rect.centery
        # print(self.rect.top)
        
        angle = math.atan2(mouse_posY, -mouse_posX) 
        # print(angle)
        angle = math.degrees(angle)
        # print(angle)
        self.image = pygame.transform.rotate(self.image, angle + 90)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        targetPost = mouse_pos
        # print(targetPost)
        # self.rect.x = targetPost[0]
        # self.rect.y = targetPost[1]
