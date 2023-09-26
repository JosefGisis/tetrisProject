"""
This module contains interactive surfaces using the Pygame library.
Use Surfaces.info() to get information.
"""

# TODO: add feature that checks if the mouse has gone of the screen surface
import pygame
pygame.init()
# screen = pygame.display.set_mode((1000, 800))


def info():
    print("\nButton(surface, location, image1, image2, relative_pos=(0, 0)"
          "\n> surface parameter: blitting surface for Button object."
          "\n> image1 and image2 parameter: default image and hovering image."
          "\n> relative_pos parameter: should equal surface left and right for mouse location checking."
          "\nButton.update_button(): displays button and checks for user interactivity."
          "\n\nTextButton(self, surface, rect, text, relative_pos=(0, 0))"
          "\n\nWarningBox(self, surface, rect, message)"
          "\nWarningBox.display_box(): displays warning box."
          "\nWarningBox.button1_rect(): returns the location and dimensions for an optional button (one of two)."
          "\nWarningBox.button2_rect(): returns the location and dimensions for an optional button (two of two).")


"""
Interactive button class.
Takes blit surface target, location, and two images. The second image appears when the cursor is hovering over the
button (add the same image to skip this feature)
The update button function checks if the mouse is clicked for the first time and if the cursor is hovering over the
button's rect and returns true if conditions are met. Otherwise, the default button image is displayed.
"""


class Button:
    def __init__(self, surface, location, image1, image2, relative_pos=(0, 0)):
        self.surface = surface
        self.image1, self.image2 = image1, image2
        self.left, self.top = location
        self.right, self.bottom = self.left + self.image1.get_width(), self.top + self.image1.get_height()
        self.relative_pos = relative_pos
        self.clicked = False

    def update_button(self):
        self.surface.blit(self.image1, (self.left, self.top))  # displays default image
        if not pygame.mouse.get_pressed()[0]:  # checks if player is holding down mouse key
            self.clicked = False
        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        # adjusts mouse position by the relative position of the surface
        mouse_pos = mouse_posx - self.relative_pos[0], mouse_posy - self.relative_pos[1]
        if self.left <= mouse_pos[0] <= self.right and self.top <= mouse_pos[1] <= self.bottom:
            # if hovering, image2 is displayed
            self.surface.blit(self.image2, (self.left, self.top))
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True


"""
Interactive button class.
Takes blit surface target, location, and button text. 
The update button function checks if the mouse is clicked for the first time and if the cursor is hovering over the
button's rect and returns true if conditions are met.
"""


class TextButton:
    def __init__(self, surface, rect, text, relative_pos=(0, 0)):
        self.surface = surface
        self.left, self.top, self.width, self.height = rect
        self.right, self.bottom = self.left + self.width, self.top + self.height
        self.button_surf = pygame.Surface((self.width, self.height))
        self.relative_pos = relative_pos
        self.clicked = False

        self.text_font = pygame.font.SysFont("ocraextended", self.height // 2)
        self.text_surf = self.text_font.render(text, True, (255, 255, 255))
        self.text_left = (self.width - self.text_surf.get_width()) // 2
        self.text_top = (self.height - self.text_surf.get_height()) // 2

    def update_button(self):
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        mouse_pos = mouse_posx - self.relative_pos[0], mouse_posy - self.relative_pos[1]
        if self.left <= mouse_pos[0] <= self.right and self.top <= mouse_pos[1] <= self.bottom:
            self.button_surf.fill((75, 25, 100))
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
        else:
            self.button_surf.fill((50, 0, 75))
        self.button_surf.blit(self.text_surf, (self.text_left, self.text_top))
        self.surface.blit(self.button_surf, (self.left, self.top))


class WarningBox:  # warning dialogue box class
    def __init__(self, surface, rect, message):
        self.surface = surface  # surface where the warning box will be blitted
        self.left, self.top, self.width, self.height = rect

        # warning box surface object
        self.box = pygame.Surface((self.width, self.height))

        # message surface and properties
        # msg font is determined by a coefficient (1.2), the width of the box, and the size of the message
        self.msg_font = pygame.font.SysFont("ocraextended", int(self.width / len(message) * 1.2))
        self.msg_surf = self.msg_font.render(message, True, (255, 255, 255))
        self.msg_left, self.msg_top = (self.width - self.msg_surf.get_width()) // 2, int(0.2 * self.height)

    def display_box(self):  # displays warning box
        self.box.blit(self.msg_surf, (self.msg_left, self.msg_top))
        self.surface.blit(self.box, (self.left, self.top))

    def button1_rect(self):  # returns rect for one of two optional buttons
        # button width is 1/4 width and 1/8 the height of the warning box
        button_width, button_height = self.width // 4, self.height // 8
        # left is determined by dividing the warning box width into 20 segments and placing buttons at intervals
        button1_left = (self.width // 20) * 4
        button_top = (self.height // 8) * 5
        return button1_left, button_top, button_width, button_height

    def button2_rect(self):  # returns rect of of two of two optional buttons
        button_width, button_height = self.width // 4, self.height // 8
        button2_left = (self.width // 20) * 11
        button_top = (self.height // 8) * 5
        return button2_left, button_top, button_width, button_height


"""
exit_warning = WarningBox(screen, (800, 300, 500, 300), "QUIT GAME?")
# using exit warning box to determine location and dimensions of buttons
ok_btn = TextButton(exit_warning.box, exit_warning.button1_rect(), "MAYBE?", (exit_warning.left, exit_warning.top))
cancel_btn = TextButton(exit_warning.box, exit_warning.button2_rect(), "CANCEL", (exit_warning.left, exit_warning.top))

print(isinstance(exit_warning, WarningBox))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    exit_warning.display_box()
    if ok_btn.update_button():
        running = False
    cancel_btn.update_button()
    pygame.display.flip()

pygame.quit()
"""