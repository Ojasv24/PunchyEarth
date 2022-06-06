import math
import pygame
import pymunk


class Astroids(pygame.sprite.Sprite):
    def __init__(self, space, postion, gravityPostion, gravityForce, color) -> None:
        super().__init__()
        # pymunk

        # body
        self.body = pymunk.Body()
        self.body.position = postion
        self.body.mass = 0.0001
        self.body.moment = 1
        self.body.velocity_func = self.limit_velocity

        # shape
        self.shape = pymunk.Circle(self.body, 30)
        self.shape.collision_type = 2

        # variables
        self.gravityPostion = gravityPostion
        self.gravityForce = gravityForce
        self.ass = 30
        self.color = color
        space.add(self.body, self.shape)

    def draw(self, screen):
        pygame.draw.circle(screen,
                           self.color,
                           self.body.position, self.shape.radius)
        
        pygame.draw.arc(screen, self.color, pygame.Rect(960 - 200, 540 - 200,
                        400, 400), self.ass + math.pi / 2, self.ass + math.pi / 2 + 0.10, 12)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 200
        pymunk.Body.update_velocity(body, gravity, 1, dt)
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
