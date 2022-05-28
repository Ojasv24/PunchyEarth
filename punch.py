import pygame
import math


class Punch(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('1.png'))
        self.sprites.append(pygame.image.load('2.png'))
        self.sprites.append(pygame.image.load('3.png'))
        self.sprites.append(pygame.image.load('4.png'))
        self.sprites.append(pygame.image.load('5.png'))
        self.sprites.append(pygame.image.load('6.png'))
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (50, 90))

        self.vel = 10
        self.dx = 0
        self.dy = 0
        self.prevx = pos_x
        self.prevy = pos_y
        self.distance = 0
        self.punchAngle = 0
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def angle(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_posX = mouse_pos[0]
        mouse_posY = mouse_pos[1]
        mouse_posX = mouse_posX - self.rect.centerx
        mouse_posY = mouse_posY - self.rect.centery

        newangle = math.atan2(mouse_posY, -mouse_posX)
        newangle1 = math.atan2(mouse_posY, mouse_posX)
        self.punchAngle = math.degrees(newangle)
    
        self.distance = int(math.hypot(
            mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery) / self.vel)
        self.dx = math.cos(newangle1) * self.vel
        self.dy = math.sin(newangle1) * self.vel

    def move(self):
        if self.distance:
            self.distance -= 1
            self.prevx += self.dx
            self.prevy += self.dy

    def update(self, pos_x, pos_y):
        pass
        # animation
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.rotate(self.image, self.punchAngle + 90)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.prevx
        self.rect.centery = self.prevy
        self.move()
