"""
button class for generating interactive buttons.
Takes blit surface target, location, and two images. The second image appears when the cursor is hovering over the
button (add the same image to skip this feature)
The update button function checks if the mouse is clicked for the first time and if the cursor is hovering over the
button's rect and returns true is conditions are met. Otherwise, the default button image is displayed.
"""

import pygame, sys
pygame.init()


def help():
    help_message = """\nbutton.Button() creates a button object that returns True when the cursor is hovering over the
    \rbutton surface and the left mouse button is depressed.\n\nbutton.Button(self, surface, location, image1, image2)
    \rsurface: surface blitting destination\rimage1: default button image
    \rimage2: displayed when the cursor is hovering over the button (add the same to skip this feature)"""
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