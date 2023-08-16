"""This is the main file for my project"""

import pygame, random

pygame.init()

display_size = (1000, 800)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("PLACEHOLDER ITEM")
pygame.time.Clock()

banner_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 75)
score_font = pygame.font.Font(None, 35)
menu_bg = pygame.image.load("bg.jpg")
resized_bg = pygame.transform.scale(menu_bg, display_size)

def start_menu():
    running = True
    while running:
        screen.blit(resized_bg, [0 ,0])
        """
        Below are the three buttons for the start menu
        """
        start_button = pygame.surface.Surface([30, 30])
        start_button.fill((0,0,0))
        start_button.convert()
        """
        Below is a list of messages to be displayed on the start menu (these may be placed
        in a list at some later time).     
        
        The positions (pos) are set in the middle of the screen by by subtracting the width
        of the screen with the width of the message and diving that by two. Buttom messages
        can be centered by using the height of the buttons as well.
        
        The True arguement in the render function is for anti aliasing.
        """
        title_msg = "PLACEHOLDER TITLE"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen.get_width() - title_surf.get_width())/2), 100)

        start_msg = "START"
        start_surf = button_font.render(start_msg, True, (255, 255, 255))
        start_pos = (0, 0) #Place holder position

        help_msg = "HELP & INFO"
        help_surf = button_font.render(help_msg, True, (255, 255, 255))
        help_pos = (0, 0)

        exit_msg = "EXIT"
        exit_surf = button_font.render(exit_msg, 1, (255, 255, 255))
        exit_pos = (0, 0)

        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

start_menu()
"""def help_and_info():

def game():

def pause_menu():

def game_over():

game_state = "menu"

while True:
    if game_state == "menu":
        start_menu()
    elif game_state == "help":
        help_and_info()
    elif game_state == "game":
        game()
    elif game_state == "pause":
        pause_menu()
    else game_state == "over":
        game_over()"""
