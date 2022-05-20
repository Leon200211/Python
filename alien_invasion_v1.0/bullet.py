import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''класс для управления пулями'''

    def __init__(self, ai_settins, screen, ship):
        '''создание обькта пули'''
        super().__init__()
        self.screen = screen

        # создание пули в позиции
        self.rect = pygame.Rect(0, 0 , ai_settins.bullet_width, ai_settins.bullet_height)   # создание пули с нуля
        self.rect.centerx = ship.rect.centerx  # пуля спавнится где корабыль
        self.rect.top = ship.rect.top

        # позиция пули по вертикали хранится в вещественном формате
        self.y = float(self.rect.y)

        # настройки цвета и скорости пули
        self.color = ai_settins.bullet_color
        self.speed_factor = ai_settins.bullet_speed_factor


    def update(self):
        '''перемещает пулю вверх по эрану'''
        self.y -= self.speed_factor
        # обновление позиции прямоугольницк
        self.rect.y = self.y

    def draw_bullet(self):
        '''вывод пули на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)



