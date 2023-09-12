"""
This is some practice for the main game loop of my tetris projects.
Quick note: Tetromino refers to the seven different tetris shapes, each shape is associated with a letter, tetro is
short for tetromino, segment refers to one of the four parts of each tetromino, matrix refers to the list of lists that
structures each tetromino shape, and surface (regarding segments) refers to images displayed on each segment to enhance
their appearance and give them colors.
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
    """
    The following code ensures the next tetromino is displayed in the center of the next piece surface. O requires
    custom logic because O if offset within its matrix, so that it displayed at the correct starting point on the play
    play surface. However this cause to not be properly display on the next piece surface.
    """
    if next_letter != O_PIECE:
        start = ((next_surface_width - (segment_size * len(next_letter))) // 2)
    else:
        start = (((next_surface_width - segment_size * 2) // 2) - segment_size)
    for row in range(len(next_letter)):
        for column in range(len(next_letter)):
            if next_letter[row][column] == 1:
                """
                The horizontal location is set to be in the center, but the vertical location is pushed down to allow
                for room for the surface banner.
                """
                location = [(start + (segment_size * column)), (3 * segment_size + (segment_size * row))]
                new_segment = Segment(location, next_surface)
                next_tetro.add(new_segment)


"""
After each piece has dropped this function is called to check where it has landed. This is required so that falling
tetrominos can be compared against the grid matrix to see if it has been blocked. The grid matrix will also be used to
check if any lines have been completed.
"""


def check_pos():
    global grid
    for segment in current_tetro.sprites():
        grid_xpos, grid_ypos = (segment.rect.left // segment_size), (segment.rect.top // segment_size + 2)
        grid[grid_ypos][grid_xpos] = 1


"""
Dropped_segments and update_surface are responsible for handling each tetro and the game loop, once the tetro lands.
Each segment is transferred to dropped_segments, the current tetro is emptied, variables startx and starty are reset,
current_letter and current_surface take their values from the next tetromino, a new tetro is generated, the rotation
status is set to its spawn state, and a new next tetromino is created.
"""
dropped_segments = pygame.sprite.Group()


def update_surface():
    global starty, startx, current_tetro, dropped, next_letter, next_surface, current_letter, current_surface, \
        rotation_state
    for segment in current_tetro.sprites():
        dropped_segments.add(segment)
    current_tetro.empty()
    startx, starty = (3 * segment_size), (-2 * segment_size)
    current_letter, current_surface = next_letter, next_surface
    gen_tetro(current_letter, current_surface)
    next_tetro.empty()
    gen_next()
    dropped = 0
    rotation_state = 0


"""
The move_blocked function checks if the tetro can make another move. The function checks if the piece can move without
being blocked by adding the xspeed and yspeed variables (speed refers to the jump size and direction). If the function
returns true, the move is blocked (see README file for more information on collision detection).
"""


def move_blocked(xspeed, yspeed):
    for segment in current_tetro:
        """
        Checks the tetromino if it will be blocked by the right or left wall or floor of the play surface. The next
        location is obtained by taking the tetro's current location ans adds the xspeed and yspeed respectively.
        """
        next_location = [(segment.rect.left + xspeed), (segment.rect.top + yspeed)]
        if next_location[0] < 0 or next_location[0] >= play_surface_width or next_location[1] >= play_surface_height:
            return True
        """
        The function checks if the tetromino is going to collide with any dropped tetrominos. 
        """
        for square in dropped_segments:
            if next_location[0] == square.rect.left and next_location[1] == square.rect.top:
                return True


"""
The three shift functions move each square by a given size and updates the startx or starty variables to keep track of
the pieces location (startx and starty are used when a new tetromino is generated after each rotation (see README for 
more information)). Shift down increments the dropped variable if its descent is blocked. When the dropped variable
meets the grace_period variable, the piece has officially landed and a new piece is generated. The purpose of the 
dropped variable is to give the player a grace period to adjust the tetro after it has dropped.  
"""


def shift_right():
    global startx
    if dropped < grace_period:
        if not move_blocked(segment_size, 0):
            for segment in current_tetro.sprites():
                segment.rect.centerx += segment_size
            startx += segment_size


def shift_left():
    global startx
    if dropped < grace_period:
        if not move_blocked(-segment_size, 0):
            for segment in current_tetro.sprites():
                segment.rect.centerx -= segment_size
            startx -= segment_size


"""
Shift down has a special optional argument that checks if the user is speeding up the descent of the tetromino. When the
player performs an accelerated drop dropped, the dropped variable may shorten the duration the user can adjust the tetro
after its drop. The optional argument slows down the grace period. However, if the player continues to hold down the 
accelerated descent button after the tetro has dropped, the grace period will still be shortened. Future versions may 
correct this detail.
"""


def shift_down(increment=10):
    global dropped, starty
    if move_blocked(0, segment_size):
        dropped += increment
    else:
        for segment in current_tetro.sprites():
            segment.rect.centery += segment_size
        starty += segment_size


"""
This function instantly drops the falling tetromino. The player is given no grace period.
"""


def hard_drop():
    global dropped
    while not move_blocked(0, segment_size):
        shift_down()
        dropped = grace_period


"""
This function handles the clockwise rotation of the current tetro. The function first checks to make sure the current
tetro is not the o piece (see documentation for O constant) and that the tetro has not landed yet. The function uses
list comprehension to transpose the rows and columns and reverse the order of each row. This rotates the letter matrix
by ninety degrees (see documentation for more information). A new tetro is generated, using the updated matrix, at the
same spot using the tracking variables startx and starty. Then the function checks if the tetro has exceeded the
boundaries of the right or left walls or the floor of the play surface. If there is a collision each piece is tested in
multiple locations (see lists below for location tests) until there is no longer a collision. If the piece cannot be
cleared, the collision fails. The logic behind the loop is too detailed for a full explanation; please check out the
README file for a full explanation.This is the first version and will probably be improved later.

Do not alter any check lists. Lists are calibrated to ensure tetrominos do not exceed play surface boundaries or collide
with dropped tetrominos.
"""
# TODO: test different rotation testing patterns

cw_check = [[[0, 1], [-1, -1], [2, 0], [-1, -1], [0, 1]], [[1, 0], [-1, 1], [0, -2], [-1, 1], [1, 0]],
            [[0, -1], [1, 1], [-2, 0], [1, 1], [0, -1]], [[-1, 0], [1, -1], [0, 2], [1, -1], [-1, 0]]]

cw_ipiece_check = [[[0, 2], [0, -3], [-2, 1], [3, 0], [-1, 0]], [[2, 0], [-3, 0], [1, 2], [0, -3], [0, 1]],
                   [[0, -2], [0, 3], [2, -1], [-3, 0], [1, 0]], [[-2, 0], [3, 0], [-1, -2], [0, 3], [0, -1]]]

ccw_check = [[[0, 1], [1, -1], [-2, 0], [1, -1], [0, 1]], [[1, 0], [-1, -1], [0, 2], [-1, -1], [1, 0]],
             [[0, -1], [-1, 1], [2, 0], [-1, 1], [0, -1]], [[-1, 0], [1, 1], [0, -2], [1, 1], [-1, 0]]]

ccw_ipiece_check = [[[0, 2], [0, -3], [2, 1], [-3, 0], [1, 0]], [[2, 0], [-3, 0], [1, -2], [0, 3], [0, -1]],
                    [[0, -2], [0, 3], [-2, -1], [3, 0], [-1, 0]], [[-2, 0], [3, 0], [-1, 2], [0, -3], [0, 1]]]

"""
See README file for a detailed explanation of the rotation functions.
"""
# TODO: break rotation into smaller functions


def cw_rotation():
    global current_letter, rotation_state, startx, starty
    blocked = False
    if current_letter != O_PIECE and dropped < grace_period:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))]
                          for i in range(len(current_letter[0]))]
        for list in rotated_letter:
            list.reverse()
        gen_tetro(rotated_letter, current_surface)
        if move_blocked(0, 0):
            if len(current_letter) < len(I_PIECE):
                for i in range(len(cw_check)):
                    if i == rotation_state:
                        for j in range(len(cw_check[i])):
                            for segment in current_tetro:
                                segment.rect.left += (cw_check[i][j][0] * segment_size)
                                segment.rect.top -= (cw_check[i][j][1] * segment_size)
                            startx += (cw_check[i][j][0] * segment_size)
                            starty -= (cw_check[i][j][1] * segment_size)
                            if move_blocked(0, 0):
                                blocked = True
                            else:
                                blocked = False
                                break
            else:
                for i in range(len(cw_ipiece_check)):
                    if i == rotation_state:
                        for j in range(len(cw_ipiece_check[i])):
                            for segment in current_tetro:
                                segment.rect.left += (cw_ipiece_check[i][j][0] * segment_size)
                                segment.rect.top -= (cw_ipiece_check[i][j][1] * segment_size)
                            startx += (cw_ipiece_check[i][j][0] * segment_size)
                            starty -= (cw_ipiece_check[i][j][1] * segment_size)
                            if move_blocked(0, 0):
                                blocked = True
                            else:
                                blocked = False
                                break

        if not blocked:
            current_letter = rotated_letter
            if rotation_state < 3:
                rotation_state += 1
            else:
                rotation_state = 0
        else:
            gen_tetro(current_letter, current_surface)


def ccw_rotation():
    global current_letter, rotation_state, startx, starty
    blocked = False
    if current_letter != O_PIECE and dropped < grace_period:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter[0]))]
                          for i in range(len(current_letter))]
        rotated_letter.reverse()
        gen_tetro(rotated_letter, current_surface)
        if move_blocked(0, 0):
            if len(current_letter) < len(I_PIECE):
                for i in range(len(ccw_check)):
                    if i == rotation_state:
                        for j in range(len(cw_check[i])):
                            for segment in current_tetro:
                                segment.rect.left += (ccw_check[i][j][0] * segment_size)
                                segment.rect.top -= (ccw_check[i][j][1] * segment_size)
                            startx += (ccw_check[i][j][0] * segment_size)
                            starty -= (ccw_check[i][j][1] * segment_size)
                            if move_blocked(0, 0):
                                blocked = True
                            else:
                                blocked = False
                                break
            else:
                for i in range(len(ccw_ipiece_check)):
                    if i == rotation_state:
                        for j in range(len(ccw_ipiece_check[i])):
                            for segment in current_tetro:
                                segment.rect.left += (ccw_ipiece_check[i][j][0] * segment_size)
                                segment.rect.top -= (ccw_ipiece_check[i][j][1] * segment_size)
                            startx += (ccw_ipiece_check[i][j][0] * segment_size)
                            starty -= (ccw_ipiece_check[i][j][1] * segment_size)
                            if move_blocked(0, 0):
                                blocked = True
                            else:
                                blocked = False
                                break

        if not blocked:
            current_letter = rotated_letter
            if rotation_state > 0:
                rotation_state -= 1
            else:
                rotation_state = 3
        else:
            gen_tetro(current_letter, current_surface)


"""
Most of the variables are declared in this section. Letter matrices are declared along with surfaces for the sake of
clarity. Each letter (tetromino shape) has an image associated with it.
"""
I_PIECE = [[0, 0, 0, 0],
           [1, 1, 1, 1],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
i_surface = pygame.image.load("teal_segment.jpg")

J_PIECE = [[1, 0, 0],
           [1, 1, 1],
           [0, 0, 0]]
j_surface = pygame.image.load("blue_segment.jpg")

L_PIECE = [[0, 0, 1],
           [1, 1, 1],
           [0, 0, 0]]
l_surface = pygame.image.load("orange_segment.jpg")

T_PIECE = [[0, 1, 0],
           [1, 1, 1],
           [0, 0, 0]]
t_surface = pygame.image.load("purple_segment.jpg")

"""
O does not rotate. The matrix is larger than the shape to offset the tetro to start at the correct position.
"""
O_PIECE = [[0, 1, 1],
           [0, 1, 1],
           [0, 0, 0]]
o_surface = pygame.image.load("magenta_segment.jpg")

S_PIECE = [[0, 1, 1],
           [1, 1, 0],
           [0, 0, 0]]
s_surface = pygame.image.load("green_segment.jpg")

Z_PIECE = [[1, 1, 0],
           [0, 1, 1],
           [0, 0, 0]]
z_surface = pygame.image.load("red_segment.jpg")

tetro_list = (I_PIECE, J_PIECE, L_PIECE, T_PIECE, O_PIECE, S_PIECE, Z_PIECE)
tetro_surfaces = (i_surface, j_surface, l_surface, t_surface, o_surface, s_surface, z_surface)

"""
Segment size is the size of each tetromino segment and is essential to most other aspect of the program. The start 
location of each tetro, play surface size, movement size, etc. are determined by segment_size. Rotation state is the
rotation degree of each tetromino (0, 90, 180, and 270). The rotation state of each piece affects its rotation
behaviour. Current letter and next letter belong to the current tetro and next tetro respectively (same for the next
surface and current surface). startx and starty keep track of the top left corner of each tetromino and keep track of
the location of each current tetromino for when they are regenerated after each successful rotation (see rotation 
functions). These need to be stored as global variables rather than attributes because each tetro is tracked as sprite
group rather than a specific class. The grid matrix keeps track of the location of dropped tetrominos. The grid is two
rows higher than the size of the play surface because tetros start two segment sizes of the play surface.
"""
segment_size = 36
rotation_state = 0
current_letter = 0
next_letter = 0
next_surface = 0
current_surface = 0
starty = (-2 * segment_size)
startx = (3 * segment_size)

# TODO: grid may not be necessary
# TODO: create list of dropped tetromino rows

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

"""
Moving and grace_period coordinate falling pieces. If dropped is less than grace_period the pieces is still falling, 
else the piece has dropped and a new piece is called. The grace_period variable allows the user to have a couple of 
moments for movement even if the piece has been blocked. THe seperate variable dropped and blocked allows the piece to
be stopped when it hits a barrier but still gives the user some loops for adjustments. USEREVENT is a custom event used 
in a timer event later on. The key_delay, previous_shift_time, previous_drop_time, shift_interval, and drop_interval 
variables are used in the game loop to mimic the pygame.key.set_repeat function (see later documentation).
"""
dropped = grace_period = 50
key_delay = 150
prev_shift_time = 50
prev_drop_time = 50
shift_interval = 50
drop_interval = 40
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
next_surface_size = next_surface_width, next_surface_height = ((segment_size * 5), (segment_size * 6))
pygame.display.set_caption("TITLE PLACEHOLDER")
clock = pygame.time.Clock()
bg_img = pygame.transform.scale(pygame.image.load("bg.jpg"), display_size)
pygame.time.set_timer(USEREVENT, 250)

"""
Sets the first next tetro. This starts the cycle of current and next tetro generation.
"""
gen_next()


def start_game():
    global prev_shift_time, prev_drop_time
    clock.tick(30)
    running = True
    while running:
        """
        if dropped checks to see if the tetro has landed yet. It it has not, the program checks for user input. Else the
        a new piece is generated. The else condition displays the next tetromino and assigns a new tetromino to fall.
        The fall also checks if the user has cancelled the game.
        """

        # TODO: create loop to handle game over function
        # TODO: create ESC event to handle user pauses

        if dropped < grace_period:
            """
            Game controls are subject to change. Currently controls are: key_right shifts tetro to the right,
            key_left shifts the tetro to the left, d rotates the tetro clockwise, a rotates the tetro counterclock-
            wise. s accelerates the tetro's descent, space instantly drops the tetro, and escape changes the game
            state to the pause menu.
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        """
                        The time_clicked_r variable is used to compare the time the right arrow key is pressed to the
                        duration of the user holding down the key. time_clicked_r as well as the other timing variables
                        below function as a delay for when the user holds down the direction keys.
                        """
                        time_clicked_r = pygame.time.get_ticks()
                        shift_right()
                    elif event.key == pygame.K_LEFT:
                        time_clicked_l = pygame.time.get_ticks()
                        shift_left()
                    elif event.key == pygame.K_s:
                        time_clicked_s = pygame.time.get_ticks()
                    elif event.key == pygame.K_d:
                        cw_rotation()
                    elif event.key == pygame.K_a:
                        ccw_rotation()
                    elif event.key == pygame.K_SPACE:
                        hard_drop()
                elif event.type == USEREVENT:
                    shift_down()

            """
            Pygame offers a key.set_repeat function but I could not use it because it does not differentiate between
            different keys. Therefore, I need to mimic the set_repeat function in the following code. 
            Pygame's get_pressed() function returns a list containing the current keys being depressed. The code below, 
            checks if the right, left, or s keys are being depressed. The if loops create a delay and interval effect
            for the keys by checking when the button has initially been depressed and by checking when the tetro has
            previously moved.
            """
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RIGHT]:
                """
                time_clicked_r is the time the right button had started being depressed and then checks the current time
                and then checks if it has exceeded the key_delay variable. The and expression evaluates how much time
                has passed from the previous shift. If shift_interval is exceeded, the tetro is moved and the previous
                shift time is reassigned.
                """
                if pygame.time.get_ticks() - time_clicked_r >= key_delay\
                        and pygame.time.get_ticks() - prev_shift_time >= shift_interval:
                    shift_right()
                    prev_shift_time = pygame.time.get_ticks()
            if pressed_keys[pygame.K_LEFT]:
                if pygame.time.get_ticks() - time_clicked_l >= key_delay\
                        and pygame.time.get_ticks() - prev_shift_time >= shift_interval:
                    shift_left()
                    prev_shift_time = pygame.time.get_ticks()
            if pressed_keys[pygame.K_s]:
                if pygame.time.get_ticks() - time_clicked_s >= key_delay - 50\
                        and pygame.time.get_ticks() - prev_drop_time >= shift_interval:
                    """
                    Shift down is passed a one millisecond argument to extend the grace period.
                    """
                    shift_down(1)
                    prev_drop_time = pygame.time.get_ticks()

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
            pygame.draw.rect(screen, (0, 0, 0), [((screen_width - play_surface_width) // 2) - 6,
                                                 ((screen_height - play_surface_height) // 2) - 6,
                                                 play_surface_width + 11, play_surface_height + 11])
            screen.blit(play_surface, (((screen_width - play_surface_width) // 2),
                                       ((screen_height - play_surface_height) // 2)))
            screen.blit(next_tetro_surface, ((((right_margin - next_surface_width) // 2) + play_surface_right),
                                             ((screen_height - play_surface_height) // 2)))

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            check_pos()
            update_surface()
    pygame.quit()


start_game()
