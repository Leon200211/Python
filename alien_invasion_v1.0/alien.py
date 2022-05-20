import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settinsgs = ai_settings

        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def blime(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''возвращает True если пришелец у края'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        self.x += (self.ai_settinsgs.alien_speed_factor * self.ai_settinsgs.fleet_direction)
        self.rect.x = self.x
