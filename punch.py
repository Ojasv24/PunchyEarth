import math
from typing import Tuple
import pygame
import pymunk

FORCE = 1000


class Punch(pygame.sprite.Sprite):
    # size = (50,90)
    def __init__(self, space, size: Tuple, gravityPostion: Tuple, group: int) -> None:
        super().__init__()

       # pygame
        self.sprites = [pygame.image.load(f'{i}.png') for i in range(1, 7)]
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], size)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [100, 100]

        # pymunk

        # body
        self.body = pymunk.Body()
        self.body.position = (300, 300)
        self.body.mass = 1
        self.body.moment = 1
        self.body.velocity_func = self.limit_velocity

        # shape
        self.vertices = [(20, 10), (10, 10), (10, 10)]
        img_h, img_w = self.sprites[0].get_width(
        ), self.sprites[0].get_height()
        self.shape = pymunk.Poly.create_box(self.body, (img_w, img_h))
        self.shape.elasticity = 50
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(group=group)

        # variables
        self.targetPos = 0, 0
        self.clicked = False
        self.returning_back = True
        self.gravityPostion = gravityPostion

        space.add(self.body, self.shape)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 1000
        pymunk.Body.update_velocity(body, gravity, 0.99, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

    def returnBack(self):
        self.returning_back = True
        self.targetPos = self.gravityPostion

    def go_to_mouse(self):
        if not self.clicked:
            self.clicked = True
            mouse_pos = pygame.mouse.get_pos()
            self.targetPos = mouse_pos
            self.returning_back = False
            mx, my = self.targetPos
            bx, by = self.body.position
            angle = math.atan2(mx - bx, my - by)
            self.body.angle = -(angle + math.pi / 2)

    def draw(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        self.image = pygame.transform.rotate(
            self.image, math.degrees(-(self.body.angle - 1 / 2 * math.pi)))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position

    def update(self):
        mx, my = self.targetPos
        bx, by = self.body.position
        angle = math.atan2(mx - bx, my - by)

        ba = -(angle + math.pi / 2) - self.body.angle
        fx, fy = math.sin(angle) * FORCE, math.cos(angle) * FORCE

        self.body.apply_force_at_world_point((fx, fy), (0, 0))
        dist = math.sqrt((mx - bx)**2 + (my - by) ** 2)

        if self.returning_back and dist < 50:
            self.body.velocity = (0, 0)
            self.body.position = self.gravityPostion
            self.returning_back = False
            self.clicked = False
        elif self.clicked and dist < 50:
            self.returnBack()

        self.body.torque = ba * 20
        self.body.angular_velocity = math.copysign(
            min(abs(self.body.angular_velocity), 10), self.body.angular_velocity)
        if abs(ba) < 0.1:
            self.body.angular_velocity = 0

        vertices = []
        for v in self.shape.get_vertices():
            x, y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x, y))
        self.vertices = vertices

        self.draw()
