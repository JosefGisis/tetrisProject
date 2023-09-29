"""
This module contains interactive surfaces using the Pygame library.
Use Surfaces.info() to get information.
"""

# TODO: add feature that checks if the mouse has gone of the screen surface
import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))


def info():
    print("\nButton(self, surface, location, image1, image2, relative_pos=(0, 0)"
          "\n> surface parameter: blitting surface for Button object."
          "\n> image1 and image2 parameter: default image and hovering image."
          "\n> relative_pos parameter: should equal surface left and right for mouse location checking."
          "\nButton.update_button(): displays button and checks for user interactivity."
          "\n\nTextButton(self, surface, rect, text, relative_pos=(0, 0))"
          "\n\nWarningBox(self, surface, rect, message)"
          "\nWarningBox.display_box(): displays warning box."
          "\nWarningBox.button1_rect(): returns the location and dimensions for an optional button (one of two)."
          "\nWarningBox.button2_rect(): returns the location and dimensions for an optional button (two of two)."
          "\n\nTextBox(self, surface, text, rect)"
          "\n> text parameter: takes text for display (preferably from a text file)."
          "\nTextBox.layout_text(): sets up text layout."
          "\nTextBox.update_box(): checks for user input and displays text."
          "\nTextBox.scroll(self, speed): allows other user inputs to scroll through text."
          "\n> speed parameter: set custom scroll speed (set positive or negative).")


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
This is a textbox class. It takes a text (preferably through a text files) and displays it in the text box. If the
text size exceeds the size of the window, the text becomes scrollable. 
"""


class TextBox:
    def __init__(self, surface, text, rect):
        self.surface = surface
        self.text = text
        self.text_top = 20  # text size (controls text movement and boundaries)
        self.word_surfs, self.word_pos = [], []  # list of word objects and word object locations
        self.font = pygame.font.Font(None, 30)
        # surface attributes
        (self.left, self.top, self.width, self.height) = rect
        self.text_surface = pygame.Surface((self.width, self.height))
        # the following variables control the scroll bar attributes and scrolling behaviour
        self.scroll_range = self.text_height = self.height - 40  # text height defaults to scroll range
        (self.scroll_left, self.scroll_top, self.scroll_height) = (self.width - 20, 20, self.height - 40)
        self.holding_scroll = False
        # by default the scroll ratio is 1 (meaning the text is the same size as the scroll range)
        self.scroll_ratio = self.scroll_range // self.text_height
        self.clicked = self.in_range = False
        self.layout_text()  # layout text function

        """
        Laying out text is a relatively large task so it is given its own function. Once the text is laid out, the
        scrollbar height and scroll ratio are adjusted. The text surface is adjusted to ensure it is a whole multiple
        of the surface area (see below).   
        """

    def layout_text(self):
        x_pos, y_pos = 20, 0  # starting position for text
        lines = self.text.split("\n")
        for line in lines:
            words = line.split(" ")  # seperate line by spaces, yielding individual words
            for word in words:
                word_surf = self.font.render(word, True, (255, 255, 255))
                if word_surf.get_width() + x_pos >= (self.scroll_left - 10):  # checks if lines width exceeds surface width
                    y_pos += word_surf.get_height() + 10  # moved text a line down
                    x_pos = 20  # sets text back to its leftmost position
                self.word_surfs.append(word_surf)  # adds word to word list
                self.word_pos.append((x_pos, y_pos))  # adds words location to parallel array
                x_pos += word_surf.get_width() + 10  # spaces words apart
            y_pos += 30
            x_pos = 20
        self.text_height = y_pos + 20  # assigns text height
        # the following code ensures text height is evenly divisible by height of scroll range
        if self.text_height % self.scroll_range != 0:
            self.text_height += self.scroll_range - (self.text_height % self.scroll_range)  # next evenly divisible
        self.scroll_ratio = self.text_height // self.scroll_range  # sets scroll ratio
        self.scroll_height = self.scroll_range // self.scroll_ratio  # resizes scroll bar based on scroll ratio

        """
        This function checks for user interaction with the scrollbar and displays the text accordingly. The 
        scroll bar can be moved once it is selected even if the mouse is not above the bar.
        """

    def update_box(self):
        # checks if player has released mouse button and gets current position for later comparison
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            self.in_range = False
            pygame.mouse.get_rel()
            self.holding_scroll = False  # player has released hold
        # gets relative position of mouse
        mouse_xpos, mouse_ypos = pygame.mouse.get_pos()
        mouse_pos = mouse_xpos - self.left, mouse_ypos - self.top
        # checks if user hovers over buttons and grabs hold of scroll bar
        if (self.scroll_left - 10) <= mouse_pos[0] <= (self.scroll_left + 20):
            if 20 <= mouse_pos[1] <= (self.height - 20):
                if self.scroll_top <= mouse_pos[1] <= (self.scroll_top + self.scroll_height):
                    if pygame.mouse.get_pressed()[0] and not self.clicked or self.in_range:
                        self.in_range = False
                        self.clicked = True
                        self.holding_scroll = True
                else:
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.in_range = True
                        dif = mouse_pos[1] - self.scroll_top - (self.scroll_height // 2)
                        self.scroll(dif)
        # while holding scroll bar and hovering over scroll range
        if self.holding_scroll and 20 <= mouse_pos[1] <= (self.height - 20):
            difference = pygame.mouse.get_rel()[1]
            self.scroll(difference)
        self.display_box()
        if pygame.mouse.get_pressed()[0]:
            self.clicked = True

    def display_box(self):
        self.text_surface.fill((40, 40, 40))
        for i in range(len(self.word_surfs)):
            self.text_surface.blit(self.word_surfs[i], (self.word_pos[i][0], self.word_pos[i][1] + self.text_top))
        pygame.draw.rect(self.text_surface, (200, 200, 200),
                         (self.scroll_left, self.scroll_top, 10, self.scroll_height))
        self.surface.blit(self.text_surface, (self.left, self.top))

    def scroll(self, speed):
        if speed > 0 and (self.scroll_top + self.scroll_height) < (self.height - 20):
            if (speed + self.scroll_top + self.scroll_height) > (self.height - 20):
                speed = (self.height - 20) - (self.scroll_top + self.scroll_height)
            self.scroll_top += speed
            self.text_top -= speed * self.scroll_ratio
        elif speed < 0 and self.scroll_top >= 20:
            if (self.scroll_top + speed) < 20:
                speed = 20 - self.scroll_top
            self.scroll_top += speed
            self.text_top -= speed * self.scroll_ratio

info()
with open("textbox", "r+") as f:
    message = f.read()

text_box = TextBox(screen, message, (100, 100, 800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                text_box.scroll(-10)
            elif event.button == 5:
                text_box.scroll(10)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                text_box.scroll(12)
            elif event.key == pygame.K_UP:
                text_box.scroll(-12)
    screen.fill((255, 255, 255))
    text_box.update_box()
    pygame.display.flip()

pygame.quit()