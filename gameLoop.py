"""This is the main file for my project"""

import sys, pygame, random

pygame.init()
display_size = screen_width, screen_height = (1000, 800)  #screen size is assigned to a variable for ease of manipulation
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("TITLE PLACEHOLDER")
pygame.time.Clock()

"""
This segment contains information in use throughout the program.
"""

color_dict = {"black": (0, 0, 0), "white": (255, 255, 255), "purple": (208, 48, 217),
              "dark purple": (75, 25, 100), "darker purple": (50, 0, 75), "red": (227, 11, 33),
              "teal": (13, 209, 180), "blue": (14, 97, 240), "green": (8, 199, 24),
              "magenta": (199, 8, 126), "coral": (255, 127, 80)}
I = [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

J = [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]]
L = [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]]

T = [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]]

O = [[0, 1, 1],
     [0, 1, 1],
     [0, 0, 0]]

S = [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]]

Z = [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]]
tetro_list = [I, J, L, T, O, S, Z]
main_font = "ocraextended"
copyrite_font = pygame.font.Font(None, 30)
banner_font = pygame.font.SysFont(main_font, 80)
score_font = pygame.font.SysFont(main_font, 35)
bg_img = pygame.transform.scale(pygame.image.load("bg.jpg"), display_size)

"""
This is a button class that uses pygame's draw.rect function. This class allows the user to create
buttons with a custom size, position, font, text, and corner roundness. However, the fact that this class
uses a draw function rather than than a rect or surface object comes with some limitations (namely that
I cannot reference a rect object).

The button text is a seperate function because it allows the flexibility to generate the text individually. This
is especially useful when the program needs to update the button.

The update button functions checks if the mouse is hovering over the button and returns True if it is. The
function checks if the mouse is within the self.left, top, width, height attributes rather than checking the
coordinates of the button because I used a draw function rather than a Rect object.   
"""

class Drawnbutton:
    def __init__(self, surface, color, dimensions, text):
        pygame.draw.rect(surface, color, dimensions, 0, 7)
        self.left, self.top, self.width, self.height = dimensions[0], dimensions[1], dimensions[2], dimensions[3]
        self.text = text

    def button_text(self, color, font):
        button_font_size = int(self.height * 0.80) #scales size of text based on button size
        button_font = pygame.font.SysFont(font, button_font_size)
        button_text_surf = button_font.render(self.text, True, color) #True confirms anti aliasing
        """
        This code finds the placement of the text by comparing the size of the text compared to the 
        button and finds its staring positions.
        """
        button_text_pos = [(((self.width - button_text_surf.get_width()) // 2) + self.left),
                           (((self.height - button_text_surf.get_height()) // 2) + self.top)]
        screen.blit(button_text_surf, button_text_pos)

    def update_button(self, color):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.left and mouse_pos[0] <= (self.left + self.width):
            if mouse_pos[1] >= self.top and mouse_pos [1] <= (self.top + self.height):
                pygame.draw.rect(screen, color, [self.left, self.top, self.width, self.height], 0, 7)
                return True
            else: return None
        else: None

def new_game():
    pass

def start_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #checks if the mouse is being depressed
                """checks if any of the buttons are returning a hovering states (e.g. select start)
                which means the player is hovering over that particular button."""
                if select_start:
                    state = "start"
                    return state
                elif select_help:
                    state = "help and info"
                    return state
                elif select_exit:
                    state = "exit"
                    return state
                else: None
            else: None

        screen.blit(bg_img, (0, 0))
        """
        >>> Below is a list of messages to be displayed on the start menu (these may be placed
        in a list at some later time).     
        >>> The positions (pos) are set in the middle of the screen by by subtracting the width
        of the screen with the width of the message and diving that by two. Buttom messages
        can be centered by using the height of the buttons as well.
        """
        title_surf = banner_font.render("TITLE PLACEHOLDER", True, color_dict["white"])
        title_pos = (((screen_width - title_surf.get_width())/2), 150)
        screen.blit(title_surf, title_pos)
        copyrite_surf = copyrite_font.render("©️ 2023 Josef Gisis", True, color_dict["white"])
        copyrite_pos = (((screen_width - copyrite_surf.get_width())/2), 625)
        screen.blit(copyrite_surf, copyrite_pos)
        """
        >>> Below are the three buttons for the start menu
        >>> I will probably include a button update function that checks to see if the
        mouse position is hovering over the area of the button and will update the 
        color of the button if it is. Because the update is called each frame, when
        the mouse is no longer hovering over the button the buttons will be set back
        to their darker shades.
        >>> This update function will work alongside the event handler to see if the mouse
        button is being depressed. When it is depressed the button will also change the 
        game state. 
        This is also the first method for displaying these buttons. Later updates may include
        a loop to deal with the buttons. A loop would require tha drawnbutton class to be
        updated as well.
        Each button contains an initializing function, an update function, and text function.
        Each variable and function is associated with the button's name for clarity.
        """
        button_left = (screen_width - 500) / 2 #gets the starting point of the button
        button_width = 500
        button_height = 75
        start_button = Drawnbutton(screen, color_dict["darker purple"],
                                   [button_left, 315, button_width, button_height],"START")
        select_start = start_button.update_button(color_dict["dark purple"])
        start_button.button_text(color_dict["white"], main_font)

        help_button = Drawnbutton(screen, color_dict["darker purple"],
                                  [button_left, 415, button_width, button_height], "HELP & INFO")
        select_help = help_button.update_button(color_dict["dark purple"])
        help_button.button_text(color_dict["white"], main_font)

        exit_button = Drawnbutton(screen, color_dict["darker purple"],
                                  [button_left, 515, button_width, button_height], "EXIT")
        select_exit = exit_button.update_button(color_dict["dark purple"])
        exit_button.button_text(color_dict["white"], main_font)

        pygame.display.flip()

    pygame.quit()

"""
This is the main game loop.
"""
def start_game():
    falling = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "main menu"
                    return game_state

        screen.blit(bg_img, (0, 0))
        play_surface_size = (play_surface_width, play_surface_height) = (360, 720)
        play_surface = pygame.Surface((play_surface_size))
        screen.blit(play_surface, (((screen_width - play_surface_width) // 2),
                                       ((screen_height - play_surface_height) // 2)))
        if falling:
            pass


        pygame.display.flip()
    pygame.quit()
def pause_menu():
    pass

"""This is a placeholder function"""
def game_over():
    running = True
    while running:

        screen.blit(bg_img, [0, 0])

        title_msg = "GAME OVER"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen_width - title_surf.get_width()) / 2), 325)
        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "main menu"
                    return game_state

        pygame.display.flip()

    pygame.quit()

"""This is a placeholder function"""
def help_and_info():
    running = True
    screen.fill((0, 0, 0))
    while running:

        title_msg = "HELP & INFO"
        title_surf = banner_font.render(title_msg, True, (255, 255, 255))
        title_pos = (((screen_width - title_surf.get_width()) // 2), ((screen_height - title_surf.get_height()) // 2))
        screen.blit(title_surf, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "main menu"
                    return game_state

        pygame.display.flip()

    pygame.quit()

"""
This is the central loop that controls the state of the game. Each state of the game
has a function (e.g. start game, game over, menu), and the game state is controlled by 
a return variable within each function.

Once an event assigns a new game state to the game state variable, the function returns
the game state and starts a new function.

The pause menu and game over screen may be changed to be contained within the game loop.
"""
game_state = "main menu"
while True:
    if game_state == "main menu":
        game_state = start_menu()
    elif game_state == "help and info":
        game_state = help_and_info()
    elif game_state == "start":
        game_state = start_game()
    elif game_state == "pause menu":
        game_state = pause_menu()
    elif game_state == "game over":
        game_state = game_over()
    elif game_state == "exit":
        pygame.quit()
