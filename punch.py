import math
import pygame
import pymunk


class Punch(pygame.sprite.Sprite):

    def __init__(self, space) -> None:
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

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [100, 100]
        self.sprite_angle = 0
        
        self.vertices = [(20, 10), (10, 10), (10, 10)]
        self.body = pymunk.Body()
        self.body.position = (300, 300)
        self.body.mass = 10
        self.body.moment = 100
        self.mousePos = 0, 0
        
        sh, sw = self.sprites[0].get_width(), self.sprites[0].get_height()
        self.body.velocity_func = self.limit_velocity
        self.shape = pymunk.Poly.create_box(self.body, (sw, sh))
        # self.shape.elasticity = 5
        self.shape.density = 100
        self.shape.collision_type = 1 
        
        space.add(self.body, self.shape)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 200
        pymunk.Body.update_velocity(body, gravity, 0.9, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

    
    def returnBack(self):
        self.mousePos = 640, 360
        mouse_pos = 640, 360
        mouse_pos = mouse_pos - self.body.position
        newangle = math.atan2(mouse_pos[1], -mouse_pos[0])
        self.sprite_angle = math.degrees(newangle)
        

    def cal_angel(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mousePos = mouse_pos
        mouse_pos = mouse_pos - self.body.position
        newangle = math.atan2(mouse_pos[1], -mouse_pos[0])
        self.sprite_angle = math.degrees(newangle)
    
    def update(self):


        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.rotate(self.image, self.sprite_angle + 90)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position
        
        mx, my = self.mousePos
        bx, by = self.body.position
        angle = math.atan2(mx - bx, my - by)
        self.body.angle = -(angle + math.pi / 2)
        


 
        fx, fy = math.sin(angle) * 1000000000, math.cos(angle) * 1000000000
        self.body.apply_force_at_world_point((fx, fy), (10, 0))
        dist = math.sqrt((mx - bx)**2 + (my - by) ** 2)

        if dist < 5 and self.body.velocity[0] < 4 and self.body.velocity[1] < 4:
            self.body.velocity = (0, 0)
            self.body.torque = 0
            self.body.angular_velocity = 0

        vertices = []
        for v in self.shape.get_vertices():
            x, y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x, y))
        self.vertices = vertices
