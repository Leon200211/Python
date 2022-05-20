'''основной файл игры'''

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # создание игрового окна
    background_image = pygame.image.load('images/test.jpg')
    pygame.init()
    ai_settings = Settings()
    pygame.display.set_caption(ai_settings.display_set_caption)  # передаем название окна из класса Settings из модуля settings
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height, ) # передаем размеры окна из класса Settings
    )
    # создание корабля
    ship = Ship(ai_settings, screen) # создаем экземпляр корабля

    sb = Scoreboard(ai_settings, screen, stats)

    # создание кнопки
    play_button = Button(ai_settings, screen, 'Play')


    # создаие групы для хранения пуль и пришельцев
    bullets = Group()
    aliens = Group()

    # создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # создание пришельца
    alien = Alien(ai_settings, screen)



    # Основной цикл игры
    while True:
        ''' 
            1 считывает действия
            2 обновления корабля
            3 вывод и удаление пуль
            4 вывод картинки  
        '''
        gf.cheak_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)  # обрабатывает нажатия клавиш и событий мыши

        if stats.game_active == True:
            ship.update()  # обновляет позицию кораблся при действии игрока
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)  # изменяет изображение на экране и отображает новый экран



run_game()