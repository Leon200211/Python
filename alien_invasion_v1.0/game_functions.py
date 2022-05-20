'''игровой движок'''

import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def fire_bullet(ai_settings, screen, ship, bullets):
    # создание новой пули и включение ее в группу bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # создаение новой пули через файл bullet.py
        bullets.add(new_bullet)  # добавление новой пули в группу

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Реагирует на нажатие кравиш'''
    if event.key == pygame.K_RIGHT:
        # перемешаем корабыль вправо
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)





def cheak_keyup_events(event, ship):
    '''Реагирует на отпускание клавиш'''
    if event.key == pygame.K_RIGHT:  # если эта правая кнопка значение moving_right становится равным False
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:  # если эта левая кнопка значение moving_left становится равным False
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()  # закрыть систему


def cheak_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    '''обрабатывает нажатия клавиш и событий мыши'''
    for event in pygame.event.get():  # цикл событий pygame.event.get() используется для получения доступа к событию
        if event.type == pygame.QUIT:  # если мышка кликнула на кнопку закрытия
            sys.exit()  # закрыть систему
        elif event.type == pygame.KEYDOWN:  # если нажата кнопка на клавиатуре
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:    # если нажатая кнопка отпускается
            cheak_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active =True

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship,aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()  # обновляет позицию пуль на экране
    # удаление пуль
    for bullet in bullets.copy():  # метод copy() используется для создания цикла в котором можно изменять содиржимое группы bullets
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)  # удаляет пулю из группы если она достигла конца экрана
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)




def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # проверка попаданий в пришельцев
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()


    if len(aliens) == 0:
        # уничтожение существующих пуль и создание нового флота
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''изменяет изображение на экране и отображает новый экран'''
    screen.fill(ai_settings.bg_color)  # передаем цвет фона окна
    # все пули выводятся позади изображений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    sb.show_score()

    ship.blitme()  # перересовка корабля
    aliens.draw(screen)  # перересовка вражеского корабля

    if not stats.game_active:
        play_button.draw_button()


    pygame.display.flip()  # показывает последний отресованый экран






# ==========================================================================
# оченб важная функция для создания врагов

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width      # вычисление количества пришельцев
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """определение количествва рядов помещающихся на экрате"""
    available_space_y = (ai_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Создание пришельца и размешения его в ряду'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''создание флота пришельцев'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)


    # создание флота пришельцев
    for row_nuber in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_nuber)



def cheak_fleet_edges(ai_settings, aliens):
    """"реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges() == True:
            change_fleet_direction(ai_settings, aliens)
            break  # очень важно

def change_fleet_direction(ai_settings, aliens):
    """опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """обработка столкновения кораблся с пришельцами"""
    if stats.ships_left > 0:
        # уменьшение ships_left
        stats.ships_left -= 1
        # очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # создание нового флота и размещение кораблся в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # добавляем паузу
        sleep(1.0)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''проверяет добрались ли пришельцы до нижней части экрана'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    '''Проверяет достиг ли флот края экрана после чего меняет позицию пришельцев'''
    cheak_fleet_edges(ai_settings, aliens)
    aliens.update()

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

