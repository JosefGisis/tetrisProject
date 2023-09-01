"""
This is some practice for the main game loop of my tetris projects.
Quick note: Tetromino refers to the seven different tetris shapes, each shape is associated with a letter, tetro is
short for tetromino, segment refers to one of the four parts of each tetromino, matrix refers to the list of lists that
structures each tetromino shape, and surface (in regards to segments) refers to images displayed on each segment to
enhance their appearance and give them colors.
"""
import sys, pygame, random

"""
This is the segment class for all tetrominos. Throughout the program, segment refers to all of the four parts each     
tetromino is made up of. The Segment class takes a location and surface argument to generate each piece.
"""


class Segment(pygame.sprite.Sprite):
    def __init__(self, location, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


"""
Current tetro is the is the pygame group that is responsible for the current or falling tetromino (throughout the
program, tetro is always referring to tetromino). Current_tetro is declared right before the gen_tetro function for the
sake of clarity. gen_tetro is cleared before each iteration because of the cw and ccw rotation function (see later). The
function checks the current letter and creates a segment at the correct location. The location is determined by the loop
and preset variable labeled startx and starty.
"""
current_tetro = pygame.sprite.Group()


def gen_tetro(letter, surface):
    global starty, startx
    current_tetro.empty()
    for row in range(len(letter)):
        for column in range(len(letter)):
            if letter[row][column] == 1:
                location = [(startx + (segment_size * column)), (starty + (segment_size * row))]
                new_segment = Segment(location, surface)
                current_tetro.add(new_segment)


"""
Same as the previous function, next_tetro is a sprite group declared before its respective function for the sake of 
clarity. Each tetro is generated along with the next tetro. The gen_next function assigns the shape of the tetro as well
as the color (referred to as surface). Rather than being displayed on the play surface, the next tetro is displayed on a
board meant to display the next piece. The location expression is temporary a will be corrected later.
"""
next_tetro = pygame.sprite.Group()


def gen_next():
    global next_letter, next_surface
    """
    Next_letter is picked from the list of letters and the program retrieves the correct segment surface by getting the
    letter's index and matching it to a parallel tuple.
    """
    next_letter = random.choice(tetro_list)
    next_surface = tetro_surfaces[tetro_list.index(next_letter)]
    for row in range(len(next_letter)):
        for column in range(len(next_letter)):
            if next_letter[row][column] == 1:
                location = [(segment_size + (segment_size * column)), (segment_size + (segment_size * row))]
                new_segment = Segment(location, next_surface)
                next_tetro.add(new_segment)


"""
Dropped_segments and update_surface are responsible for handling each tetro and the game loop, once the tetro lands.
Each segment is transferred to dropped_segments, the current tetro is emptied, variables startx and starty are reset,
current_letter and current_surface take their values from the next tetromino, a new tetro is generated, and a new next
tetromino is created.
"""
dropped_segments = pygame.sprite.Group()


def update_surface():
    global starty, startx, current_tetro, moving, next_letter, next_surface, current_letter, current_surface
    for segment in current_tetro.sprites():
        dropped_segments.add(segment)
    current_tetro.empty()
    startx, starty = (3 * segment_size), (-2 * segment_size)
    current_letter, current_surface = next_letter, next_surface
    gen_tetro(current_letter, current_surface)
    next_tetro.empty()
    gen_next()
    moving = True


"""
This function moves the tetro to the right. It checks if the tetro has hit the right wall, and if it has not, the tetro
is shifted to the right. The startx variable is also updated, so a new tetromino can be updated at the same position.
The shift_right function also makes the leftmost condition false because the piece has been moved away from the right
wall.
"""


def shift_right():
    global current_tetro, rightmost, leftmost, startx
    if moving == True:
        for segment in current_tetro.sprites():
            if segment.rect.right >= play_surface_width:
                rightmost = True
        if rightmost == False:
            for segment in current_tetro.sprites():
                segment.rect.centerx += segment_size
            startx += segment_size
            leftmost = False


"""
See previous doc.
"""


def shift_left():
    global current_tetro, leftmost, rightmost, startx
    if moving == True:
        for segment in current_tetro.sprites():
            if segment.rect.left <= 0:
                leftmost = True
        if leftmost == False:
            for segment in current_tetro.sprites():
                segment.rect.centerx -= segment_size
            startx -= segment_size
            rightmost = False


"""
See previous doc.
"""


def shift_down():
    global current_tetro, moving, starty
    for segment in current_tetro.sprites():
        if segment.rect.bottom >= play_surface_height:
            moving = False
    if moving == True:
        for segment in current_tetro.sprites():
            segment.rect.centery += segment_size
        starty += segment_size


"""
This function handles the clockwise rotation of the current tetro. The function first checks to make sure the current
tetro is not the o piece (see documentation for O constant) and that the tetro has not landed yet. The function uses
list comprehension to transpose the rows and columns and reverse the order of each row. This rotates the letter matrix
by ninety degrees (more information can be found by looking into matrix rotation algorithms). A new tetro is generated,
using the updated matrix, at the same spot using the tracking variables startx and starty. 
"""


def cw_rotation():
    global current_letter, current_surface, O
    if current_letter != O and moving:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))] for i in range(len(current_letter[0]))]
        for list in rotated_letter:
            list.reverse()
        current_letter = rotated_letter
        gen_tetro(current_letter, current_surface)


"""
Same as the previous function. The rows and columns are transposed. However, unlike the previous function, the rows are
reversed rather than the contents of each row being reversed.
"""


def ccw_rotation():
    global current_letter, current_surface, O
    if current_letter != O and moving:
        rotated_letter = [[current_letter[j][i] for j in range (len(current_letter[0]))] for i in range(len(current_letter))]
        rotated_letter.reverse()
        current_letter = rotated_letter
        gen_tetro(current_letter, current_surface)


"""
Most of the varables are declared in this section. Letter matrices are declared along with surfaces for the sake of
clarity. Each letter (tetromino shape) has an image associated with it.
"""
I = [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
i_surface = pygame.image.load("teal_segment.jpg")

J = [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]]
j_surface = pygame.image.load("blue_segment.jpg")

L = [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]]
l_surface = pygame.image.load("coral_segment.jpg")

T = [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]]
t_surface = pygame.image.load("purple_segment.jpg")

"""
O does not rotate. The matrix is larger than the shape to offset the tetro to start at the correct position.
"""
O = [[0, 1, 1],
     [0, 1, 1],
     [0, 0, 0]]
o_surface = pygame.image.load("magenta_segment.jpg")

S = [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]]
s_surface = pygame.image.load("green_segment.jpg")

Z = [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]]
z_surface = pygame.image.load("red_segment.jpg")

tetro_list = (I, J, L, T, O, S, Z)
tetro_surfaces = (i_surface, j_surface, l_surface, t_surface, o_surface, s_surface, z_surface)

"""
Segment size is fundamental to the program. It is the size of each tetromino segment. The start location of each tetro,
play surface size, movement size, etc. are determined by segment_size.
"""
segment_size = 36
starty = (-2 * segment_size)
startx = (3 * segment_size)

"""
Moving, leftmost, rightmost check if the the tetro has hit the right or left wall or the floor. USEREVENT is a custom
event used in a timer event later on.
"""
moving = False
leftmost = False
rightmost = False
USEREVENT = 24

pygame.init()
display_size = screen_width, screen_height = (1000, 800)
screen = pygame.display.set_mode(display_size)

"""
These are some variables to set the size of the play surface, as well determine the right and bottom boundaries of the
play surface. The right and bottom borders help determine the right border of the display. The right margin helps 
determine where other surfaces can be displayed.
"""
play_surface_size = (play_surface_width, play_surface_height) = ((segment_size * 10), (segment_size * 20))
play_surface_right, play_surface_bottom = (((screen_width - play_surface_width) // 2) + play_surface_width), \
                                          (((screen_height - play_surface_height) // 2) + play_surface_height)
right_margin = (screen_width - play_surface_right)
next_surface_size = next_surface_width, next_surface_height = ((segment_size * 5), (segment_size * 5))
pygame.display.set_caption("TITLE PLACEHOLDER")
pygame.time.Clock()
bg_img = pygame.transform.scale(pygame.image.load("bg.jpg"), display_size)
pygame.time.set_timer(USEREVENT, 250)

"""
Sets the first next tetro. This starts the cycle of current and next tetro generation.
"""
gen_next()


def start_game():
    global rightmost, leftmost
    running = True
    while running:
        """
        if moving checks to see if the tetro has landed yet. It it has not, the program checks for user input. Else the
        a new piece is generated. The else condition also checks if the user has cancelled the game.
        """
        if moving:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        shift_right()
                    elif event.key == pygame.K_LEFT:
                        shift_left()
                    elif event.key == pygame.K_d:
                        cw_rotation()
                    elif event.key == pygame.K_a:
                        ccw_rotation()
                elif event.type == USEREVENT:
                    shift_down()
            """
            All the tetro pieces are displayed, as well as the surfaces. The pieces are first displayed on their 
            respective surfaces, then the respective surfaces are displayed.
            """
            screen.blit(bg_img, (0, 0))
            play_surface = pygame.Surface(play_surface_size)
            next_tetro_surface = pygame.Surface(next_surface_size)
            current_tetro.draw(play_surface)
            dropped_segments.draw(play_surface)
            next_tetro.draw(next_tetro_surface)
            screen.blit(play_surface, (((screen_width - play_surface_width) // 2),
                                       ((screen_height - play_surface_height) // 2)))
            screen.blit(next_tetro_surface, ((((right_margin - next_surface_width) // 2) + play_surface_right),
                                             ((screen_height - play_surface_height) // 2)))

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            update_surface()
    pygame.quit()

start_game()

