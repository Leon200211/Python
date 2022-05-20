'''космический корабыль '''

import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        self.screen = screen

        # загрузка изображения
        self.image = pygame.image.load('images/alien_ship.png')  # загружает картину в код
        self.rect = self.image.get_rect()     # получаем атрибут rect (представляем обьект прямоугольником)
        self.screen_rect = screen.get_rect()  # сохраняем прямоугольник экрана в self.screen_rect
        self.ai_settings = ai_settings  # передаем из главного фаила ai_settings = Settings()
        # каждый новый корабыль появляется у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)  # создаем новый параметр который ссылается на rect.center но в float
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        '''этот метод выводит корабыль на экран'''
        self.screen.blit(self.image, self.rect)  # выводит изображение в позиции заданой self.rect

    def update(self):
        '''передвижение корабля'''
        if self.moving_right == True and self.rect.right < self.screen_rect.right: # передвигаем корабыль если условие выполняется
            self.center += self.ai_settings.ship_speed_factor  # корабыль передвигается если кнопка зажата
        elif self.moving_left == True and self.rect.left > 0:
           self.center -= self.ai_settings.ship_speed_factor  # (изменяем параметр с момощью класса Settings)

        # обновления атрибута rect на основе self.center
        self.rect.centerx = self.center         # передаем координаты

    def center_ship(self):
        """размешает корабль в центре нижней стороны"""
        self.center = self.screen_rect.centerx

