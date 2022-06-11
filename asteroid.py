import math
import pygame
import pymunk

from collision_handler import asteroid


class asteroids(pygame.sprite.Sprite):
    def __init__(self, space, postion, gravityPostion, gravityForce, color) -> None:
        super().__init__()

        # pygame
        self.image = pygame.image.load('./assets/astroid.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = postion

        # pymunk

        # body
        self.body = pymunk.Body()
        self.body.position = postion
        self.body.mass = 0.0006
        self.body.moment = 1

        self.body.velocity_func = self.limit_velocity

        # shape
        self.shape = pymunk.Circle(self.body, 30)
        self.shape.collision_type = asteroid

        # variables
        self.gravityPostion = gravityPostion
        self.gravityForce = gravityForce
        self.ass = 30
        self.color = color
        space.add(self.body, self.shape)

    def draw(self, screen, space):

        self.rect.center = self.body.position

        px, py = self.body.position
        gx, gy = self.gravityPostion
        rx, ry = px - gx, py - gy
        angle = math.atan2(rx, ry)
        dist = math.sqrt(rx**2 + ry**2)
        dist = 100 + dist * 0.1
        fx, fy = math.sin(angle) * dist, math.cos(angle) * dist
        pygame.draw.circle(screen,
                           self.color,
                           (fx + gx, fy + gy), 5)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 320
        pymunk.Body.update_velocity(body, gravity, 1, dt)
        # vx, vy = body.velocity
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

    def update(self):
        mx, my = self.gravityPostion
        bx, by = self.body.position
        angle = math.atan2(mx - bx, my - by)
        self.ass = angle
        fx, fy = math.sin(
            angle) * self.gravityForce, math.cos(angle) * self.gravityForce
        self.body.apply_force_at_world_point((fx, fy), (0, 0))
       