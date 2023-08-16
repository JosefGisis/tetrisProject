import pygame
pygame.init()

list = pygame.font.get_fonts()
for font in list:
    print(font)