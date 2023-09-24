"""
button class for generating interactive buttons.
Takes blit surface target, location, and two images. The second image appears when the cursor is hovering over the
button (add the same image to skip this feature)
The update button function checks if the mouse is clicked for the first time and if the cursor is hovering over the
button's rect and returns true is conditions are met. Otherwise, the default button image is displayed.
"""

import pygame, sys
pygame.init()
screen = pygame.display.set_mode((1000, 800))


def help():
    help_message = """l"""
    print(help_message)


class Button:
    def __init__(self, surface, location, image1, image2, relative_pos=(0, 0)):
        self.surface = surface
        self.image1, self.image2 = image1, image2
        self.rect1, self.rect2 = self.image1.get_rect(), self.image2.get_rect()
        self.left, self.top = location
        self.right, self.bottom = self.left + self.image1.get_width(), self.top + self.image1.get_height()
        self.relative_pos = relative_pos
        self.clicked = False

    def update_button(self):
        self.surface.blit(self.image1, (self.left, self.top))
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        mouse_pos = mouse_posx - self.relative_pos[0], mouse_posy - self.relative_pos[1]
        if self.left <= mouse_pos[0] <= self.right and self.top <= mouse_pos[1] <= self.bottom:
            self.surface.blit(self.image2, (self.left, self.top))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return True


class TextButton:
    def __init__(self, surface, rect, text, relative_pos=(0, 0)):
        self.surface = surface
        self.left, self.top, self.width, self.height = rect
        self.right, self.bottom = self.left + self.width, self.top + self.height
        self.button_surf = pygame.Surface((self.width, self.height))
        self.relative_pos = relative_pos
        self.clicked = False

        self.text_font = pygame.font.SysFont("ocraextended", int(0.5 * self.height))
        self.text_surf = self.text_font.render(text, True, (255, 255, 255))
        self.text_left = (self.width - self.text_surf.get_width()) // 2
        self.text_top = (self.height - self.text_surf.get_height()) // 2

    def update_button(self):
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        mouse_pos = mouse_posx - self.relative_pos[0], mouse_posy - self.relative_pos[1]
        if self.left <= mouse_pos[0] <= self.right and self.top <= mouse_pos[1] <= self.bottom:
            self.button_surf.fill((75, 25, 100))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return True
        else:
            self.button_surf.fill((50, 0, 75))
        self.button_surf.blit(self.text_surf, (self.text_left, self.text_top))
        self.surface.blit(self.button_surf, (self.left, self.top))


class WarningBox:
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

    # displays warning box
    def display_box(self):
        self.box.blit(self.msg_surf, (self.msg_left, self.msg_top))
        self.surface.blit(self.box, (self.left, self.top))

    # returns rect for one of two optional buttons
    def button1_rect(self):
        button_width, button_height = self.width // 4, self.height // 8
        button1_left = (self.width // 20) * 4
        button_top = (self.height // 8) * 5
        return button1_left, button_top, button_width, button_height

    # returns rect of of two of two optional buttons
    def button2_rect(self):
        button_width, button_height = self.width // 4, self.height // 8
        button2_left = (self.width // 20) * 11
        button_top = (self.height // 8) * 5
        return button2_left, button_top, button_width, button_height


exit_warning = WarningBox(screen, (200, 300, 500, 300), "WOULD YOU LIKE?")
# using exit warning box to determine location and dimensions of buttons
ok_btn = TextButton(exit_warning.box, exit_warning.button1_rect(), "OK", (exit_warning.left, exit_warning.top))
cancel_btn = TextButton(exit_warning.box, exit_warning.button2_rect(), "CANCEL", (exit_warning.left, exit_warning.top))

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