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

game_state = "menu"

class Button:
    def __init__(self, surface, color, rect, text):
        self.rect_surf = pygame.draw.rect(surface, color, rect, 0, 7)
        self.left, self.top, self.width, self.height = rect[0], rect[1], rect[2], rect[3]
        self.text = text

    def button_text(self, color):
        font_size = int(self.height * 0.90)
        button_font = pygame.font.Font(None, font_size)
        button_text_surf = button_font.render(self.text, True, color)
        text_surf_pos = [(screen.get_width() - button_text_surf.get_width()) / 2,
                         (self.height - button_text_surf.get_height()) / 2 + self.top]
        screen.blit(button_text_surf, text_surf_pos)

    def update_button(self):
        global hovering_over
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.left and mouse_pos[0] <= (self.left + self.width):
            if mouse_pos[1] >= self.top and mouse_pos [1] <= (self.top + self.height):
                self.rect_surf = pygame.draw.rect(screen, [75, 25, 100],
                                                  [self.left, self.top, self.width, self.height], 0, 7)
                hovering_over = True
                ent = self.text
                return ent
        else:
            hovering_over = False
            return None


def start_menu():
    running = True
    while running:

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
        
        I will probably include a button update function that checks to see if the
        mouse position is hovering over the area of the button and will update the 
        color of the button if it is. Because the update is called each frame, when
        the mouse is no longer hovering over the button the buttons will be set back
        to their darker shades.
        
        This update function will work alongside the event handler to see if the mouse
        button is being depressed. When it depressed the button will also change the 
        game state. 
        """
        button_left = (screen.get_width() - 500) / 2
        button_width = 500
        button_height = 75
        button_color = (50, 0, 75)
        button_text_color = [255, 255, 255]
        button1 = Button(screen, button_color, [button_left, 315, button_width, button_height], "START")
        enter1 = button1.update_button()
        button1.button_text(button_text_color)
        button2 = Button(screen, button_color, [button_left, 415, button_width, button_height], "HELP & INFO")
        enter2 = button2.update_button()
        button2.button_text(button_text_color)
        button3 = Button(screen, button_color, [button_left, 515, button_width, button_height], "EXIT")
        enter3 = button3.update_button()
        button3.button_text(button_text_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and hovering_over:
                if enter1:
                    state = "start"
                    return state
                elif enter2:
                    state = "help & info"
                    return state
                elif enter3:
                    state = "exit"
                    return state

        pygame.display.flip()

    pygame.quit()

def help_and_info():
    running = True
    while running:

        screen.blit(resized_bg, [0, 0])

        title_msg = "HELP & INFO"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen.get_width() - title_surf.get_width()) / 2), 325)
        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    return game_state

        pygame.display.flip()

    pygame.quit()

def game():
    running = True
    while running:

        screen.blit(resized_bg, [0, 0])

        title_msg = "GAME SCREEN"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen.get_width() - title_surf.get_width()) / 2), 325)
        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    return game_state

        pygame.display.flip()

    pygame.quit()


#def pause_menu():

def game_over():
    running = True
    while running:

        screen.blit(resized_bg, [0, 0])

        title_msg = "GAME OVER"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen.get_width() - title_surf.get_width()) / 2), 325)
        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    return game_state

        pygame.display.flip()

    pygame.quit()

while True:
    if game_state == "menu":
        game_state = start_menu()
    elif game_state == "help & info":
        game_state = help_and_info()
    elif game_state == "start":
        game_state = game()
    #elif game_state == "pause":
        #pause_menu()
    elif game_state == "game over":
        game_state = game_over()
    elif game_state == "exit":
        pygame.quit()
