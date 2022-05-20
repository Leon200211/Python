import sys
import pygame

def s():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('f')
    myimage = pygame.image.load('images/alien_ship.png').convert()
    background_image = pygame.image.load('images/test.jpg')

    while True:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(myimage, (200, 200))
        pygame.display.flip()

s()