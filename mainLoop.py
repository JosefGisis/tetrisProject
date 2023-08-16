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
copyrite_font = pygame.font.Font(None, 30)
menu_bg = pygame.image.load("bg.jpg")
resized_bg = pygame.transform.scale(menu_bg, display_size)

class Button:
    def __init__(self, surface, color, rect, button_text):
        button_surf = pygame.draw.rect(surface, color, rect, 0, 7)
        self.left, self.top, self.width, self.height = rect[0], rect[1], rect[2], rect[3]

    def button_text(self, button_text, color):
        font_size = int(self.height * 0.90)
        button_font = pygame.font.Font(None, font_size)
        button_text_surf = button_font.render(button_text, True, color)
        text_surf_pos = [(screen.get_width() - button_text_surf.get_width()) / 2,
                         (self.height - button_text_surf.get_height()) / 2 + self.top]
        screen.blit(button_text_surf, text_surf_pos)

def start_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(resized_bg, [0 ,0])

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
        title_pos = (((screen.get_width() - title_surf.get_width())/2), 150)
        screen.blit(title_surf, title_pos)

        copyrite_message = "©️ 2023 Josef Gisis"
        copyrite_surf = copyrite_font.render(copyrite_message, True, (255, 255, 255))
        copyrite_pos = (((screen.get_width() - copyrite_surf.get_width())/2), 625)
        screen.blit(copyrite_surf, copyrite_pos)

        """
        Below are the three buttons for the start menu
        """
        button_left = (screen.get_width() - 500) / 2
        button_width = 500
        button_height = 75
        button_color = (50, 0, 75)
        button_text_color = (255, 255, 255)
        button1 = Button(screen, button_color, [button_left, 315, button_width, button_height], "START")
        button1.button_text("START", button_text_color)
        button2 = Button(screen, button_color, [button_left, 415, button_width, button_height], "HELP & INFO")
        button2.button_text("HELP & INFO", button_text_color)
        button3 = Button(screen, button_color, [button_left, 515, button_width, button_height], "EXIT")
        button3.button_text("EXIT", button_text_color)



        pygame.display.flip()

    pygame.quit()

start_menu()
"""
def help_and_info():

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
