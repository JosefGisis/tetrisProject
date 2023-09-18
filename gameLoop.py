"""
This is some practice for the main game loop of my tetris projects.
Quick note: Tetromino refers to the seven different tetris shapes, each shape is associated with a letter, tetro is
short for tetromino, segment refers to one of the four parts of each tetromino, matrix refers to the list of lists that
structures each tetromino shape, and surface (regarding segments) refers to images displayed on each segment to enhance
their appearance and give them colors.
"""
import sys, pygame, random

"""
The new game function is responsible for resetting all game loop variables. The current_tetro empty needs to be emptied
otherwise it remains above the play surface and game over repeats. Most variables are reset when the first moving
tetromino is generated. 
"""


def new_game():
    global dropped, grace_period, game_over, score_dict, drop_rate
    current_tetro.empty()
    dropped = grace_period = 30
    drop_rate = 250
    scoreboard.reset_score([0, 1, 0, -10])
    for row in dropped_segments:
        row.empty()  # erases all the segments on the play surface
    gen_next()  # starts the next, current, next ... cycle
    game_over = False


class Scoreboard():  # this is the scoreboard object that displays and tracks scores
    def __init__(self, rect, score):  # takes the dimensions and locations and scores and creates a scoreboard object
        self.left, self.top, self.width, self.height = rect
        self.highscore, self.level, self.lines, self.score = score  # assigns scores
        self.points = (0, 100, 300, 500, 700)

    def update_score(self):
        self.score += 10  # the player gets 10 points everytime a piece is dropped
        filled_lines = get_lines()
        self.score += self.points[len(filled_lines)]  # checks filled lines to see how points player should receive
        self.lines += len(filled_lines)

    def reset_score(self, score):  # takes default scores and resets the scoreboard
        self.highscore, self.level, self.lines, self.score = score

    def display_scoreboard(self):
        """
        This function creates a scoreboard surface and displays score banners and scores. The function determines the
        location of each score by iterating through a banner list, creating the banner and score surface, and blitting
        those onto the scoreboard.
        :return:
        """
        self.surface = pygame.Surface((self.width, self.height))
        banners = ("HIGHSCORE:", "LEVEL:", "LINES:", "SCORE:")
        scores = (self.highscore, self.level, self.lines, self.score)
        for index, banner in enumerate(banners):
            banner_surface = score_font.render(banner, True, (255, 255, 255))
            score_surface = title_font.render(str(scores[index]), True, (175, 100, 255))
            self.surface.blit(banner_surface, (10, ((index * 4 * SEGMENT_SIZE) + 10)))  # text is 10 pixels from border
            self.surface.blit(score_surface, (10, ((2 * SEGMENT_SIZE) + (index * 4 * SEGMENT_SIZE) + 10)))
        screen.blit(self.surface, (self.left, self.top))


"""
The following functions and classes are responsible for creating, managing and handling current and next tetrominos.
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
and preset variable labeled tetro_left and tetro_top.
The shape of the letter is replicated by iterating through the letter matrix and creating a sprite when the index is
True (that is there is a one in that slot).
"""
current_tetro = pygame.sprite.Group()


def gen_tetro(letter, surface):
    current_tetro.empty()
    for row_index, row in enumerate(letter):
        for column_index, column in enumerate(row):
            if column:  # is there a 1 (AKA True) in that cell
                location = ((SEGMENT_SIZE * column_index) + tetro_left, (SEGMENT_SIZE * row_index) + tetro_top)
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
    next_tetro.empty()
    """
    Next_letter is picked from the list of letters and the program retrieves the correct segment surface by getting the
    letter's index and matching it to a parallel tuple.
    """
    # TODO: this randomizer does not seem to work that great
    next_letter = random.choice(TETRO_LETTERS)
    next_surface = TETRO_SURFACES[TETRO_LETTERS.index(next_letter)]
    """
    The following code ensures the next tetromino is displayed in the center of the next piece surface. O requires
    custom logic because O if offset within its matrix, so that it displayed at the correct starting point on the play
    play surface. However this cause to not be properly display on the next piece surface.
    """
    if next_letter != O_PIECE:
        left = ((next_surface_width - (SEGMENT_SIZE * len(next_letter))) // 2)
    else:
        left = (((next_surface_width - SEGMENT_SIZE * 2) // 2) - SEGMENT_SIZE)  # SEGMENT_SIZE * 2 for width of o piece
    for row_index, row in enumerate(next_letter):
        for column_index, column in enumerate(row):
            if column:
                """
                The horizontal location is set to be in the center, but the vertical location is pushed down to allow
                for room for the surface banner (by a size of 3 * SEGMENT_SIZE).
                """
                location = [((SEGMENT_SIZE * column_index) + left), ((SEGMENT_SIZE * row_index) + (3 * SEGMENT_SIZE))]
                new_segment = Segment(location, next_surface)
                next_tetro.add(new_segment)


def new_tetro():  # creates new tetro when current tetro has dropped
    global tetro_top, tetro_left, current_tetro, dropped, current_letter, current_surface, rotation_state
    tetro_left, tetro_top = (3 * SEGMENT_SIZE), (-2 * SEGMENT_SIZE)  # sets tetromino starting point
    current_letter, current_surface = next_letter, next_surface  # current tetro inherits next tetro's shape and surface
    gen_tetro(current_letter, current_surface)  # generate new current tetro
    gen_next()
    rotation_state = 0  # new tetro is dropping at its spawn state
    dropped = 0


"""
The following set of functions handle fallen tetrominos and line completion. check_pos checks the location of each tetro
after it has landed. Then the tetromino's segments are assigned to a sprite group depending on its vertical location.
The group is accessed through an index in the dropped segments list. 
get_lines returns a list of all the lines that have not been filled. The function iterates through the dropped_segments
list and iterates through each sprite group. If a group has ten segments in it, that line is added to the list.
line_animations displays a filled line animations. The function and animation will likely be changed in the future.
filled_line_handler empties all the filled rows and moves down all the above segments (see function for more
documentation).
"""


def check_pos():
    global game_over
    for segment in current_tetro.sprites():
        if segment.rect.top < 0:
            game_over = True
        else:
            dropped_segments[segment.rect.top // SEGMENT_SIZE].add(segment)  # assigns the segment to the correct row


def get_lines(): 
    return[row_index for row_index, row in enumerate(dropped_segments) if len(row) == 10]


def difficulty_level():  # this function checks if the game difficulty should be increased
    global drop_rate, grace_period
    if scoreboard.level < scoreboard.lines // 10 + 1:  # has there been a change in the level
        drop_rate -= 20  # increase drop speed
        grace_period += 5  # proportionally increase grace period
        scoreboard.level = scoreboard.lines // 10 + 1


def line_animation():  # temporary function
    filled_lines = get_lines()
    if filled_lines:
        for h in range(3):
            for j in range(45):
                for i in filled_lines:
                    screen.blit(completed_line_image1,
                                (((screen_width - play_surface_width) // 2),
                                 (i * SEGMENT_SIZE + ((screen_height - play_surface_height) // 2))))
                pygame.display.flip()
            for j in range(45):
                for i in filled_lines:
                    screen.blit(completed_line_image2,
                                (((screen_width - play_surface_width) // 2),
                                 (i * SEGMENT_SIZE + ((screen_height - play_surface_height) // 2))))
                pygame.display.flip()

"""
Filled lines handler retrieves a list of filled lines and assigns and empties the correct pygame sprite groups. It
starts from the first filled line, erases that sprite groups contents, and moves all the lines above it down. This
is repeated for all the filled lines.  
Cascading effect refers to logical errors in shifting down rows. For example: if the function were to shift rows
starting from the top row, the contents of the previous row would be placed in the following row, adding sprites that
do not belong in that row. This can mean that row contains more than ten squares. Nor can the function preemptively 
empty the contents of the following row because we have not shifted them yet. Therefor we need to shift row in reverse.
"""


def filled_lines_handler():
    filled_lines = get_lines()
    for line in filled_lines:  # starts with the first filled line
        dropped_segments[line].empty()  # empties the matching sprite group
        for i in range(line - 1, -1, -1):  # above lines are shifted down in reverse to prevent cascading effect
            for segment in dropped_segments[i].sprites():  # moves group contents to group beneath it
                dropped_segments[i + 1].add(segment)
                segment.rect.top += SEGMENT_SIZE  # repositions Square sprite
            dropped_segments[i].empty()  # empties sprite after moving contents down to prevent cascading effect


"""
The move_blocked function checks if the tetro can make another move. The function checks if the piece can move without
being blocked by adding the x_move and y_move variables (speed refers to the jump size and direction). If the function
returns true, the move is blocked (see README file for more information on collision detection).
"""


def move_blocked(x_move, y_move):
    for segment in current_tetro:
        """
        Checks the tetromino if it will be blocked by the right or left wall or floor of the play surface. The next
        location is obtained by taking the tetro's current location ans adds the x_move and y_move respectively.
        """
        next_left, next_top = (segment.rect.left + x_move), (segment.rect.top + y_move)
        if next_left < 0 or next_left >= play_surface_width or next_top >= play_surface_height:
            return True
        for row in dropped_segments:  # checks if collision with dropped tetrominos
            for square in row.sprites():
                if next_left == square.rect.left and next_top == square.rect.top:
                    return True


"""
The three shift functions move each square by a given size and updates the tetro_left or tetro_top variables to keep 
track of the pieces location (tetro_left and tetro_top are used when a new tetromino is generated after each rotation
(see README for more information)). Shift down increments the dropped variable if its descent is blocked. When the
dropped variable meets the grace_period variable, the piece has officially landed and a new piece is generated. 
The purpose of the dropped variable is to give the player a grace period to adjust the tetro after it has dropped.  
"""


def shift_right():
    global tetro_left
    if dropped < grace_period:
        if not move_blocked(SEGMENT_SIZE, 0):  # checks if piece will collide 36 pixels to the right
            for segment in current_tetro.sprites():
                segment.rect.centerx += SEGMENT_SIZE
            tetro_left += SEGMENT_SIZE  # updates the tetrominos leftmost position


def shift_left():
    global tetro_left
    if dropped < grace_period:
        if not move_blocked(-SEGMENT_SIZE, 0):  # checks if piece will collide 36 pixels to the left
            for segment in current_tetro.sprites():
                segment.rect.centerx -= SEGMENT_SIZE
            tetro_left -= SEGMENT_SIZE


"""
Shift down has a special optional argument that checks if the user is speeding up the descent of the tetromino. When the
player performs an accelerated drop dropped, the dropped variable may shorten the duration the user can adjust the tetro
after its drop. The optional argument slows down the grace period. However, if the player continues to hold down the 
accelerated descent button after the tetro has dropped, the grace period will still be shortened.
"""


def shift_down(increment=10):  # default increment of 10
    global dropped, tetro_top
    if move_blocked(0, SEGMENT_SIZE):
        dropped += increment  # when dropped = increment the piece will have landed and a new piece will be generated
    else:
        for segment in current_tetro.sprites():
            segment.rect.centery += SEGMENT_SIZE
        tetro_top += SEGMENT_SIZE



def hard_drop():  # this function instantly drops the tetromino
    global dropped
    while not move_blocked(0, SEGMENT_SIZE):  # while tetro has not hit the bottom yet
        shift_down()
        dropped = grace_period  # no grace period is given


"""
This function handles the clockwise rotation of the current tetro. The function first checks to make sure the current
tetro is not the o piece (see documentation for O constant) and that the tetro has not landed yet. The function uses
list comprehension to transpose the rows and columns and reverse the order of each row. This rotates the letter matrix
by ninety degrees (see documentation for more information). A new tetro is generated, using the updated matrix, at the
same spot using the tracking variables tetro_left and tetro_top. Then the function checks if the tetro has exceeded the
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
    global current_letter, rotation_state, tetro_left, tetro_top
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
                                segment.rect.left += (cw_check[i][j][0] * SEGMENT_SIZE)
                                segment.rect.top -= (cw_check[i][j][1] * SEGMENT_SIZE)
                            tetro_left += (cw_check[i][j][0] * SEGMENT_SIZE)
                            tetro_top -= (cw_check[i][j][1] * SEGMENT_SIZE)
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
                                segment.rect.left += (cw_ipiece_check[i][j][0] * SEGMENT_SIZE)
                                segment.rect.top -= (cw_ipiece_check[i][j][1] * SEGMENT_SIZE)
                            tetro_left += (cw_ipiece_check[i][j][0] * SEGMENT_SIZE)
                            tetro_top -= (cw_ipiece_check[i][j][1] * SEGMENT_SIZE)
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
    global current_letter, rotation_state, tetro_left, tetro_top
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
                                segment.rect.left += (ccw_check[i][j][0] * SEGMENT_SIZE)
                                segment.rect.top -= (ccw_check[i][j][1] * SEGMENT_SIZE)
                            tetro_left += (ccw_check[i][j][0] * SEGMENT_SIZE)
                            tetro_top -= (ccw_check[i][j][1] * SEGMENT_SIZE)
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
                                segment.rect.left += (ccw_ipiece_check[i][j][0] * SEGMENT_SIZE)
                                segment.rect.top -= (ccw_ipiece_check[i][j][1] * SEGMENT_SIZE)
                            tetro_left += (ccw_ipiece_check[i][j][0] * SEGMENT_SIZE)
                            tetro_top -= (ccw_ipiece_check[i][j][1] * SEGMENT_SIZE)
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


def update_play_surface():
    global play_surface
    play_surface = pygame.Surface(play_surface_size)
    current_tetro.draw(play_surface)  # uses sprite group to draw the current tetromino
    for row in dropped_segments:
        row.draw(play_surface)  # draws all the fallen pieces
    pygame.draw.rect(screen, (0, 0, 0), [((screen_width - play_surface_width) // 2) - 6,  # play surface border
                                         ((screen_height - play_surface_height) // 2) - 6,
                                         play_surface_width + 11, play_surface_height + 11])
    screen.blit(play_surface, (play_surface_left, play_surface_top))


def display_next():
    next_tetro_surface = pygame.Surface(next_surface_size)
    next_tetro.draw(next_tetro_surface)  # draw the next tetro onto the next tetro surface
    next_tetro_surface.blit(next_banner_surface,  # display next banner in the center of next piece surface
                            ((next_tetro_surface.get_width() - next_banner_surface.get_width()) // 2, 10))
    screen.blit(next_tetro_surface, ((((right_margin - next_surface_width) // 2) + play_surface_right),
                                     ((screen_height - play_surface_height) // 2)))

def display_keys():
    for key in keys:
        if key == "KEYS":
            control_surface = score_font.render(key, True, (255, 255, 255))
        else:
            control_surface = controls_font.render(key, True, (255, 255, 255))
        screen.blit(control_surface, ((((right_margin - next_surface_width) // 2) + play_surface_right),
                                      keys.index(key) * SEGMENT_SIZE + 450))

"""
This segment contains constants used throughout the game loop. 
Each letter (tetromino shape) has an image associated with it called the _____ surface. The tetro tuple and surface
tuple are parallel arrays and each tetromino has a surface associated with its shape. Segment size is the size of each
tetromino segment and is essential to most other aspect of the program. The start location of each tetro, play surface
size, movement size, etc. are determined by SEGMENT_SIZE. USEREVENT is a custom event used in a timer event within the
game loop.
"""
I_PIECE = [[0, 0, 0, 0],
           [1, 1, 1, 1],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

J_PIECE = [[1, 0, 0],
           [1, 1, 1],
           [0, 0, 0]]

L_PIECE = [[0, 0, 1],
           [1, 1, 1],
           [0, 0, 0]]

T_PIECE = [[0, 1, 0],
           [1, 1, 1],
           [0, 0, 0]]

"""
O does not rotate. The matrix is larger than the shape to offset the tetro to start at the correct position.
"""
O_PIECE = [[0, 1, 1],
           [0, 1, 1],
           [0, 0, 0]]

S_PIECE = [[0, 1, 1],
           [1, 1, 0],
           [0, 0, 0]]

Z_PIECE = [[1, 1, 0],
           [0, 1, 1],
           [0, 0, 0]]

TETRO_LETTERS = (I_PIECE, J_PIECE, L_PIECE, T_PIECE, O_PIECE, S_PIECE, Z_PIECE)
TETRO_SURFACES = (pygame.image.load("teal_segment.jpg"), pygame.image.load("blue_segment.jpg"),
                  pygame.image.load("orange_segment.jpg"), pygame.image.load("purple_segment.jpg"),
                  pygame.image.load("magenta_segment.jpg"), pygame.image.load("green_segment.jpg"),
                  pygame.image.load("red_segment.jpg"))

SEGMENT_SIZE = 36
USEREVENT = 24

"""
The KEY_DELAY and SHIFT_INTERVAL constants and the previous_shift_time and previous_drop_time variables are used in the
game loop to mimic the pygame.key.set_repeat function (see later documentation). Literal are in milliseconds. 
"""
KEY_DELAY = 150
SHIFT_INTERVAL = 60
prev_shift_time = 50
prev_drop_time = 50
drop_rate = 250

"""
This segment contains variable that control the gameloop. Some are present because they need to initialized, and some
others are only present for clarity (meaning they are first assigned a literal within the game loop). Rotation state is 
the rotation degree of each tetromino (0, 90, 180, and 270). The rotation state of each piece affects its rotation
behaviour. Current letter and next letter belong to the current tetro and next tetro respectively (same for the next
surface and current surface). tetro_left and tetro_top keep track of the top left corner of each tetromino and keep track of
the location of each current tetromino for when they are regenerated after each successful rotation (see rotation 
functions). These need to be stored as global variables rather than attributes because each tetro is tracked as sprite
group rather than a specific class. dropped_segments is a list of sprite groups that tracks all of the fallen 
tetrominos. Fallen pieces are kept in seperate groups depending on their row in order to track which lines have been
filled. game_over starts a new game when necessary. 
Dropped and grace_period coordinate falling pieces. If dropped is less than grace_period the pieces is still falling, 
else the piece has dropped and a new piece is called. The grace_period variable allows the user to have a couple of 
moments for movement even if the piece has been blocked. The seperate variable dropped and blocked allows the piece to
be stopped when it hits a barrier but still gives the user some loops for adjustments.
"""
dropped = grace_period = 30
game_over = False
rotation_state = 0
current_letter = 0
next_letter = 0
next_surface = 0
current_surface = 0
tetro_top = (-2 * SEGMENT_SIZE)
tetro_left = (3 * SEGMENT_SIZE)

dropped_segments = []
for i in range(20):
    dropped_row = pygame.sprite.Group()
    dropped_segments.append(dropped_row)

"""
Initiates all pygame modules. Display size is contained as variables for easier access. clock is an object initialized 
from Pygame's Clock class. USEREVENT is a custom timer responsible for moving the tetrominos down.
"""
pygame.init()
display_size = screen_width, screen_height = (1000, 800)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("TITLE PLACEHOLDER")
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 250)

"""
These are some variables to set the size of the play surface, as well determine the right and bottom boundaries of the
play surface. The right and bottom borders help determine the right margin. Right margin determines where other surface
can be displayed.
"""
play_surface_size = (play_surface_width, play_surface_height) = ((SEGMENT_SIZE * 10), (SEGMENT_SIZE * 20))
play_surface_left, play_surface_top = ((screen_width - play_surface_width) // 2,
                                       (screen_height - play_surface_height) // 2)
play_surface_right, play_surface_bottom = (((screen_width - play_surface_width) // 2) + play_surface_width,
                                           ((screen_height - play_surface_height) // 2) + play_surface_height)
right_margin = (screen_width - play_surface_right)

next_surface_size = next_surface_width, next_surface_height = ((SEGMENT_SIZE * 5), (SEGMENT_SIZE * 6))

title_font = pygame.font.SysFont("ocraextended", 40)
score_font = pygame.font.SysFont("ocraextended", 30)
controls_font = pygame.font.SysFont("ocraextended", 18)
keys = ["KEYS", "_______", "ESC: pause menu", "R ARROW: move right", "L ARROW: move left", "D: rotate right",
                "A: rotate left", "S: fast drop", "SPACE: hard drop"]
next_banner_surface = score_font.render("NEXT", True, (255, 255, 255))

bg_img = pygame.transform.scale(pygame.image.load("bg.jpg"), display_size)
completed_line_image1 = pygame.image.load("line_completed1.jpg")
completed_line_image2 = pygame.image.load("line_completed2.jpg")


"""
scoreboard rect sets the dimensions and locations of the scoreboard. scoreboard initializes a Scoreboard object.
gen_next sets the first next tetro. This starts the cycle of current and next tetro generation.
"""
scoreboard_rect = [((play_surface_left - SEGMENT_SIZE * 6) // 2), play_surface_top, (SEGMENT_SIZE * 6),
                   (SEGMENT_SIZE * 16 + 10)]  # the plus 10 is just the offset determined by the banners
scoreboard = Scoreboard(scoreboard_rect, [0, 1, 0, -10])
gen_next()


def start_game():
    global prev_shift_time, prev_drop_time, game_over
    clock.tick(30)
    running = True
    while running:
        if not game_over:
            """
            All the tetro pieces are displayed, as well as the surfaces. The pieces are first displayed on their 
            respective surfaces, then the respective surfaces are displayed.
            """
            screen.blit(bg_img, (0, 0))
            update_play_surface()  # function handles surface and play surface
            display_next()
            display_keys()
            scoreboard.display_scoreboard()
            pygame.display.flip()
            """
            if dropped checks to see if the tetro has landed yet. It it has not, the program checks for user input. Else
            the a new piece is generated. The else condition displays the next tetromino and assigns a new tetromino to
            fall. The fall also checks if the user has cancelled the game.
            """
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
                        game_over = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            """
                            The time_clicked_r variable is used to compare the time the right arrow key is pressed to
                            the duration of the user holding down the key. time_clicked_r as well as the other timing
                            variables below function as a delay for when the user holds down the direction keys.
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

                if pygame.time.get_ticks() - prev_drop_time >= drop_rate:
                    shift_down()
                    prev_drop_time = pygame.time.get_ticks()

                """
                Pygame offers a key.set_repeat function but I could not use it because it does not differentiate between
                different keys. Therefore, I need to mimic the set_repeat function in the following code. 
                Pygame's get_pressed() function returns a list containing the current keys being depressed. The code 
                below, checks if the right, left, or s keys are being depressed. The if loops create a delay and
                interval effect for the keys by checking when the button has initially been depressed and by checking
                when the tetro has previously moved.
                """
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_RIGHT]:
                    """
                    time_clicked_r is the time the right button had started being depressed and then checks the current
                    time and then checks if it has exceeded the KEY_DELAY variable. The and expression evaluates how 
                    much time has passed from the previous shift. If SHIFT_INTERVAL is exceeded, the tetro is moved and
                    the previous shift time is reassigned.
                    """
                    if pygame.time.get_ticks() - time_clicked_r >= KEY_DELAY\
                            and pygame.time.get_ticks() - prev_shift_time >= SHIFT_INTERVAL:
                        shift_right()
                        prev_shift_time = pygame.time.get_ticks()
                if pressed_keys[pygame.K_LEFT]:
                    if pygame.time.get_ticks() - time_clicked_l >= KEY_DELAY\
                            and pygame.time.get_ticks() - prev_shift_time >= SHIFT_INTERVAL:
                        shift_left()
                        prev_shift_time = pygame.time.get_ticks()
                if pressed_keys[pygame.K_s]:
                    if pygame.time.get_ticks() - time_clicked_s >= KEY_DELAY - 75\
                            and pygame.time.get_ticks() - prev_drop_time >= SHIFT_INTERVAL - 20:
                        """
                        Shift down is passed a one millisecond argument to extend the grace period.
                        """
                        shift_down(3)
                        prev_drop_time = pygame.time.get_ticks()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                check_pos()
                line_animation()
                scoreboard.update_score()
                difficulty_level()
                filled_lines_handler()
                new_tetro()
        else:
            new_game()
    pygame.quit()


start_game()
