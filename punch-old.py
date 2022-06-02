# import pygame
# import math
# import pymunk


# class Punch(pygame.sprite.Sprite):

#     def __init__(self, pos_x, pos_y, space) -> None:
#         super().__init__()
#         self.sprites = []
#         self.sprites.append(pygame.image.load('1.png'))
#         self.sprites.append(pygame.image.load('2.png'))
#         self.sprites.append(pygame.image.load('3.png'))
#         self.sprites.append(pygame.image.load('4.png'))
#         self.sprites.append(pygame.image.load('5.png'))
#         self.sprites.append(pygame.image.load('6.png'))
#         for i in range(len(self.sprites)):
#             self.sprites[i] = pygame.transform.scale(self.sprites[i], (50, 90))

#         # pygame
#         self.vel = 10
#         self.dx = 0
#         self.dy = 0
#         self.prevx = pos_x
#         self.prevy = pos_y
#         self.distance = 0
#         self.punchAngle = 0
#         self.current_sprite = 0
#         self.image = self.sprites[self.current_sprite]
#         self.rect = self.image.get_rect()
#         self.rect.center = [pos_x, pos_y]

#         # pymuck
#         self.body = pymunk.Body()
#         self.body.position = pos_x, pos_y
#         self.body.velocity = 100, 100
#         w, h = self.rect.right - self.rect.left, self.rect.bottom - self.rect.top
#         self.vs = [(0, 0), (w, 0), (w, h), (0, h)]
#         self.shape = pymunk.Poly(self.body, self.vs)
#         self.shape.elasticity = 1
#         self.shape.density = 5
#         self.shape.collision_type = 1
#         space.add(self.body, self.shape)

#     def angle(self):
#         mouse_pos = pygame.mouse.get_pos()
#         mouse_posX = mouse_pos[0]
#         mouse_posY = mouse_pos[1]
#         mouse_posX = mouse_posX - self.body.position[0]
#         mouse_posY = mouse_posY - self.body.position[1]

#         newangle = math.atan2(mouse_posY, -mouse_posX)
#         newangle1 = math.atan2(mouse_posY, mouse_posX)
#         self.punchAngle = math.degrees(newangle)
#         self.distance = int(math.hypot(
#             mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery) / self.vel)
#         self.dx = math.cos(newangle1) * self.vel
#         self.dy = math.sin(newangle1) * self.vel

#     def move(self):
#         if self.distance:
#             self.distance -= 1
#             self.prevx += self.dx
#             self.prevy += self.dy

#     def update(self, pos_x, pos_y):
#         pass
#         # animation
#         self.current_sprite += 0.25
#         if self.current_sprite >= len(self.sprites):
#             self.current_sprite = 0

#         self.image = self.sprites[int(self.current_sprite)]
#         self.image = pygame.transform.rotate(self.image, self.punchAngle + 90)
#         self.rect = self.image.get_rect()
#         self.rect.centerx = self.prevx
#         self.rect.centery = self.prevy
#         # self.vs = [(self.rect.topleft[0], self.rect.topleft[1]), (self.rect.bottomleft[0], self.rect.bottomleft[1]), (self.rect.bottomright[0], self.rect.bottomright[1]), (self.rect.topright[0], self.rect.topright[1])]
#         # self.shape = pymunk.Poly(self.body, self.vs,radius=5)
#         self.body.position = self.rect.midtop[0], self.rect.midtop[1]
#         self.body.angle = self.punchAngle
#         # self.body.velocity = 100,100
#         self.move()
