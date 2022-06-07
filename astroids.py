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
        # pygame.draw.arc(screen, self.color, pygame.Rect(self.gravityPostion[0] - 200, self.gravityPostion[1] - 200,
        #                 400, 400), self.ass + math.pi / 2, self.ass + math.pi / 2 + 0.10, 12)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 200
        pymunk.Body.update_velocity(body, gravity, 1, dt)
        vx, vy = body.velocity
        if vx > max_velocity:
            scale = max_velocity / vx
            body.velocity = body.velocity * scale
        if vy > max_velocity:
            scale = max_velocity / vy
            body.velocity = body.velocity * scale

    def update(self):
        mx, my = self.gravityPostion
        bx, by = self.body.position
        angle = math.atan2(mx - bx, my - by)
        self.ass = angle
        fx, fy = math.sin(
            angle) * self.gravityForce, math.cos(angle) * self.gravityForce
        self.body.apply_force_at_world_point((fx, fy), (0, 0))
