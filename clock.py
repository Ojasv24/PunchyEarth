import pygame
import time


class Clock(pygame.sprite.Sprite):
    def __init__(self, position) -> None:
        super().__init__()
        # pygame
        self.image = pygame.image.load('./assets/clock.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        #variables
        self.time = 60
        self.start = time.time()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

    def drawTime(self, screen):
        end = time.time()
        self.time = 60 - int(end - self.start)
        time_str = str(self.time)
        text_surface = self.font.render(time_str, True, (248, 188, 4))
        screen.blit(text_surface, dest=(
            self.rect.centerx + 40, self.rect.centery - 15))
