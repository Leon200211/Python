'''настройка окна'''

class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (10, 10, 10)
        self.display_set_caption = 'Alien Invasion v1.0'
        self.ship_speed_factor = 1.4  # скорость смешения коробля в пикселях
        self.ship_limit = 3  # количество жизней

        # параметры пули
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255  # цвет пули
        self.bullets_allowed = 3   # количество пуль

        self.alien_speed_factor = 0.5       # скорость пришельцев
        self.fleet_drop_speed = 10      # скоровсть снижения
        # fleet_direction = 1 обозначает движение вправо ( -1 влево)
        self.fleet_direction = 1  # направление движения

        self.alien_points = 50