"""This is the main file for my project.
Quick note: Tetromino refers to the seven different tetris shapes, each shape is associated with a letter, tetro is
short for tetromino, segment refers to one of the four parts of each tetromino, matrix refers to the list of lists that
structures each tetromino shape, and surface (regarding segments) refers to images displayed on each segment to enhance
their appearance and give them colors.
"""
import random
from surfaces import*
from tools import center
from datetime import datetime


class Score:  # this is the scoreboard object that tracks scores
    def __init__(self, banner_list, score_list, file):
        self.score_list = score_list  # assigns scores
        self.default_scores = score_list  # creates default score for each new game
        self.banner_list = banner_list  # displayed banners
        self.highscore_banner = "HIGHSCORE:"
        self.highscore = 0
        self.file = file

    def get_highscore(self):
        try:
            with open(self.file, "r") as tfile:  # tfile for try file
                first_entry = tfile.readline()  # retrieves first entry which is latest highscore
        except FileNotFoundError:
            with open(self.file, "a+") as efile:  # efile for except file
                first_entry = efile.readline()  # retrieves first entry which is latest highscore
        if first_entry:  # if there is highscore, retrieves last word of first entry (the highscore)
            self.highscore = int(first_entry.split(" ")[-1].strip("\n"))
        else:  # defaults to 0
            self.highscore = 0

    def set_highscore(self, score):
        self.highscore = score
        with open(self.file, "r") as infile:
            highscores = infile.readlines()  # retrieves highscores
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  # removes milliseconds
        new_entry = "{0} {1:-> 14}\n".format(formatted_time, self.highscore)  # formats new highscore
        highscores.insert(0, new_entry)  # places new highscore at beginning of list
        with open(self.file, "w") as outfile:
            outfile.writelines(highscores)

    def reset_score(self):  # resets the scoreboard
        self.score_list = [score for score in self.default_scores]

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
The new game function is responsible for resetting all game loop variables. The current_tetro empty needs to be emptied
otherwise it remains above the play surface and game over repeats. These are few variables to start a new game. Note,
most variables are reset when the first moving tetromino is generated in the new tetromino function. 
"""


def new_game():
    global dropped, grace_period, game_over, drop_rate, time_clicked_l, time_clicked_r, time_clicked_s
    current_tetro.empty()
    dropped = grace_period = 30
    drop_rate = 250
    time_clicked_r = time_clicked_l = time_clicked_s = 0
    scores.reset_score()
    for row in dropped_segments:
        row.empty()  # erases all the segments on the play surfaces
    gen_next()  # starts the next, current, next ... cycle
    game_over = False


"""
gen_tetro is cleared before each iteration because of the cw and ccw rotation function (see later). The
function checks the current letter and creates a segment at the correct location. The location is determined by the loop
and preset variable labeled tetro_left and tetro_top.
The shape of the letter is replicated by iterating through the letter matrix and creating a sprite when the index is
True (that is there is a one in that slot).
"""


def gen_tetro(letter, surface):
    current_tetro.empty()
    for row_index, row in enumerate(letter):
        for column_index, column in enumerate(row):
            if column:  # is there a 1 (AKA True) in that cell
                location = ((SEGMENT_SIZE * column_index) + tetro_left, (SEGMENT_SIZE * row_index) + tetro_top)
                new_segment = Segment(location, surface)
                current_tetro.add(new_segment)


"""
Each tetro is generated along with the next tetro. The gen_next function assigns the shape of the tetro as well
as the color (referred to as surface). Rather than being displayed on the play surface, the next tetro is displayed on a
board meant to display the next piece. The location expression is temporary a will be corrected later.
"""


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
        left = center(next_surface_size[0], SEGMENT_SIZE * len(next_letter))
    else:
        left = center(next_surface_size[0], SEGMENT_SIZE * 2) - SEGMENT_SIZE  # SEGMENT_SIZEx2 for width of o piece
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
    global tetro_top, tetro_left, dropped, current_letter, current_surface, rotation_state
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
    current_tetro.empty()


def get_lines():  # gets number and location of filled lines
    return[row_index for row_index, row in enumerate(dropped_segments) if len(row) == 10]


def update_score():
    points = (0, 100, 300, 500, 700)
    if not game_over:  # ensures users does not receive points after game is over
        scores.score_list[2] += 10  # the player gets 10 points everytime a piece is dropped
        filled_lines = get_lines()  # gets number of filled lines
        scores.score_list[2] += points[len(filled_lines)]  # checks filled lines to see how points player should receive
        scores.score_list[1] += len(filled_lines)


def difficulty_level():  # this function checks if the game difficulty should be increased
    global drop_rate, grace_period
    if scores.score_list[0] < scores.score_list[1] // 10 + 1:  # level increases every 10 filled rows
        # TODO: drop rate should slow down once a certain speed is hit
        drop_rate -= 20  # increase drop speed
        # TODO: grace period should match speed increase
        grace_period += 6  # proportionally increase grace period
        scores.score_list[0] = scores.score_list[1] // 10 + 1


# TODO: improve line completion animations
def line_animation():  # temporary function
    white_surface = pygame.Surface((SEGMENT_SIZE - 1, SEGMENT_SIZE - 1), pygame.SRCALPHA)
    filled_lines = get_lines()
    if not game_over:
        if filled_lines:
            white_surface.set_alpha(25)
            white_surface.fill(color_dict["white"])
            for k in filled_lines:
                for l in range(10):
                    screen.blit(white_surface, (center(screen_width, play_surface_size[0]) + l * SEGMENT_SIZE,
                                                (k * SEGMENT_SIZE + center(screen_height, play_surface_size[1]))))
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
            dropped_segments[i].empty()  # empties sprite after moving contents down to prevent cascading effect


def rows_aligned():  # checks if segment images are in their correct row and returns false if they need to be shifted
    for row_index, row in enumerate(dropped_segments):
        for segment in row.sprites():
            if segment.rect.top // SEGMENT_SIZE != row_index:
                return False
    return True


def shift_rows_down(speed):  # moves segment down incrementally (through speed)
    for row_index, row in enumerate(dropped_segments):
        for segment in row.sprites():
            if segment.rect.top // SEGMENT_SIZE != row_index:
                segment.rect.top += speed
    update_play_surface()  # redraws play surface to update their position
    pygame.display.flip()


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
        if next_left < 0 or next_left >= play_surface_size[0] or next_top >= play_surface_size[1]:
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
                segment.rect.left += SEGMENT_SIZE
            tetro_left += SEGMENT_SIZE  # updates the tetrominos leftmost position


def shift_left():
    global tetro_left
    if dropped < grace_period:
        if not move_blocked(-SEGMENT_SIZE, 0):  # checks if piece will collide 36 pixels to the left
            for segment in current_tetro.sprites():
                segment.rect.left -= SEGMENT_SIZE
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
        # TODO: create visual indication of blocked pieces
        dropped += increment  # when dropped = increment the piece will have landed and a new piece will be generated
    else:
        for segment in current_tetro.sprites():
            segment.rect.top += SEGMENT_SIZE
        tetro_top += SEGMENT_SIZE


def hard_drop():  # this function instantly drops the tetromino
    global dropped
    while not move_blocked(0, SEGMENT_SIZE):  # while tetro has not hit the bottom yet
        shift_down()
        # TODO: find a way to allow hard drop after blocked and before dropped
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

# TODO: try different wallkick pattern and experiment
# TODO: maybe relocate wallkick lists

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

# TODO: improve and simplify rotation functions


def cw_rotation():
    global current_letter, rotation_state, tetro_left, tetro_top
    blocked = False
    if current_letter != O_PIECE and dropped < grace_period:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))]
                          for i in range(len(current_letter[0]))]
        # TODO: list shadows built in function
        for matrix in rotated_letter:
            matrix.reverse()
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


# TODO: create score update board


def update_play_surface():
    play_surface.fill(color_dict["black"])
    current_tetro.draw(play_surface)  # uses sprite group to draw the current tetromino
    for row in dropped_segments:
        row.draw(play_surface)  # draws all the fallen pieces
    # Border is given one more pixel top and left because tetris pieces do not have borders top and left
    pygame.draw.rect(screen, (0, 0, 0), [center(screen_width, play_surface_size[0]) - 6,
                                         center(screen_height, play_surface_size[1]) - 6, play_surface_size[0] + 11,
                                         play_surface_size[1] + 11])
    screen.blit(play_surface, play_surface_location)


def display_scoreboard():
    """
    This function creates a scoreboard surface and displays score banners and scores. The function determines the
    location of each score by iterating through a banner list, creating the banner and score surface, and blitting
    those onto the scoreboard.
    :return:
    """
    scoreboard_surface.fill(color_dict["black"])
    # TODO: improve score_list and banner_list
    scores_list = (scores.highscore, scores.score_list[0], scores.score_list[1], scores.score_list[2])
    banners_list = (scores.highscore_banner, scores.banner_list[0], scores.banner_list[1], scores.banner_list[2])
    for index, banner in enumerate(banners_list):
        banner_surface = banner_font.render(banner, True, (255, 255, 255))
        score_surface = score_font.render(str(scores_list[index]), True, (175, 100, 255))
        # TODO: ensure large scores do not go off screen
        scoreboard_surface.blit(banner_surface, (10, ((index * 4 * SEGMENT_SIZE) + 10)))  # text 10 pixels from border
        scoreboard_surface.blit(score_surface, (10, ((2 * SEGMENT_SIZE) + (index * 4 * SEGMENT_SIZE) + 10)))
    screen.blit(scoreboard_surface, scoreboard_pos)


def display_next():
    next_tetro_surface.fill(color_dict["black"])
    next_tetro.draw(next_tetro_surface)  # draw the next tetro onto the next tetro surface
    next_tetro_surface.blit(next_text_surf, next_text_pos)
    screen.blit(next_tetro_surface, next_surface_pos)


def display_keys():
    for key_index, key in enumerate(keys):
        if key == "KEYS":
            key_surface = banner_font.render(key, True, (255, 255, 255))
        else:
            key_surface = keys_font.render(key, True, (255, 255, 255))
        screen.blit(key_surface, (center(right_margin, next_surface_size[0]) + play_surface_right,
                                  key_index * SEGMENT_SIZE + 450))


"""
declarations
________________________________________________________________________________________________________________________
"""
# initiates all pygame modules
pygame.init()
# TODO: find a way to make screen resizeable
display_size = screen_width, screen_height = (1000, 800)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("TITLE PLACEHOLDER")
clock = pygame.time.Clock()  # creates a Pygame clock object

"""
This segment contains variables/constants/objects used throughout the program
________________________________________________________________________________________________________________________
"""
SEGMENT_SIZE = 36  # segment size is based on tetro segment sizes and controls dimensions throughout the program
color_dict = {"black": (0, 0, 0), "white": (255, 255, 255), "dark purple": (75, 25, 100), "darker purple": (50, 0, 75),
              "dark gray": (40, 40, 40), "darker gray": (20, 20, 20)}
main_font = "ocraextended"
copyrite_font = pygame.font.Font(None, 30)  # small font for copyrite and version information
title_font = pygame.font.SysFont(main_font, 80)  # large font for titles
score_font = pygame.font.SysFont(main_font, 40)  # font for game scores
banner_font = pygame.font.SysFont(main_font, 35)  # banner font
keys_font = pygame.font.SysFont(main_font, 18)  # font for keys instructions
bg_img = pygame.transform.scale(pygame.image.load("images/bg.jpg"), display_size)  # bg image used throughout the game

"""
This segment contains variables/constants/objects for the main menu
________________________________________________________________________________________________________________________
"""
# TODO: create title image
# TODO: shrink and correct menu buttons
title_surf = title_font.render("TITLE PLACEHOLDER", True, color_dict["white"])
title_pos = (center(screen_width, title_surf.get_width()), 110)
copyrite_surf = copyrite_font.render("©️ 2023 Josef Gisis - v 1.1", True, color_dict["white"])
copyrite_pos = (center(screen_width, copyrite_surf.get_width()), 680)
menu_imgs = (pygame.image.load("images/menu_button1.png"), pygame.image.load("images/menu_button2.png"),
             pygame.image.load("images/menu_button3.png"), pygame.image.load("images/menu_button4.png"),
             pygame.image.load("images/menu_button5.png"), pygame.image.load("images/menu_button6.png"))
button_left = center(screen_width, menu_imgs[0].get_width())  # gets the left starting point of the button
menu_button1 = Button(screen, (button_left, 290), menu_imgs[0], menu_imgs[1])
menu_button2 = Button(screen, (button_left, 420), menu_imgs[2], menu_imgs[3])
menu_button3 = Button(screen, (button_left, 550), menu_imgs[4], menu_imgs[5])

"""
This segment contains variables/constants/constants used in the game loop.
________________________________________________________________________________________________________________________
"""
game_over = False
dropped = grace_period = 30

# The following list array constants are used in the gen_tetro function to generate letter shapes
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

# O does not rotate. The matrix is larger than the shape to offset the tetro's start location.
O_PIECE = [[0, 1, 1],
           [0, 1, 1],
           [0, 0, 0]]

S_PIECE = [[0, 1, 1],
           [1, 1, 0],
           [0, 0, 0]]

Z_PIECE = [[1, 1, 0],
           [0, 1, 1],
           [0, 0, 0]]

# parallel lists that match tetris shapes with their correct surface (each surface has a specified color)
TETRO_LETTERS = (I_PIECE, J_PIECE, L_PIECE, T_PIECE, O_PIECE, S_PIECE, Z_PIECE)
TETRO_SURFACES = (pygame.image.load("images/teal_segment.png"), pygame.image.load("images/blue_segment.png"),
                  pygame.image.load("images/orange_segment.png"), pygame.image.load("images/purple_segment.png"),
                  pygame.image.load("images/magenta_segment.png"), pygame.image.load("images/green_segment.png"),
                  pygame.image.load("images/red_segment.png"))
current_tetro = pygame.sprite.Group()  # falling tetromino group
next_tetro = pygame.sprite.Group()  # upcoming tetromino group
dropped_segments = [pygame.sprite.Group() for i in range(20)]  # sprite group array. Each group tracks one row

current_letter = current_surface = 0  # falling tetromino's letter shape and associated surface/color
next_letter = next_surface = 0  # next tetromino's letter shape and next tetromino's surface/color
rotation_state = 0  # falling tetromino's degree of rotation (0: 0, 1: 90, 2: 180, 3: 270)
tetro_left, tetro_top = (3 * SEGMENT_SIZE), (-2 * SEGMENT_SIZE)  # falling tetromino's leftmost and topmost position
animation_count = animation_length = 10  # around one sixth of a second

# TODO: some of these variables may be redundant
KEY_DELAY = 150  # used to delay hold down button feature. Literal represents milliseconds
SHIFT_INTERVAL = 60  # interval to slow tetro movement
prev_shift_time = 50  # tracks previous movement time for comparison with SHIFT_INTERVAL
prev_drop_time = 50  # track previous drop time for comparison with SHIFT_INTERVAL and drop_rate
drop_rate = 250  # controls tetromino drop rate and decreases with difficulty
time_clicked_r = time_clicked_l = time_clicked_s = 0  # tracks initial click time

# play surface and next surface dimensions
play_surface_size = SEGMENT_SIZE * 10, SEGMENT_SIZE * 20
play_surface = pygame.Surface(play_surface_size)
play_surface_location = center(screen_width, play_surface_size[0]), center(screen_height, play_surface_size[1])
play_surface_right, play_surface_bottom = play_surface_location[0] + play_surface_size[0], \
                                          play_surface_location[1] + play_surface_size[1]
right_margin = screen_width - play_surface_right  # right margin from right side of play surface
# surface for displaying upcoming tetromino
next_surface_size = SEGMENT_SIZE * 5, SEGMENT_SIZE * 6
next_tetro_surface = pygame.Surface(next_surface_size)
next_surface_pos = center(right_margin, SEGMENT_SIZE * 6) + play_surface_right,\
                    center(screen_height, play_surface_size[1])
next_text_surf = banner_font.render("NEXT", True, (255, 255, 255))
next_text_pos = center(SEGMENT_SIZE * 5, next_text_surf.get_width()), 10
# key instruction list for displaying
keys = ["KEYS", "_______", "ESC: pause menu", "R ARROW: move right", "L ARROW: move left", "D: rotate right",
                "A: rotate left", "S: fast drop", "SPACE: hard drop"]

# scoreboard rect sets the dimensions and locations of the scoreboard.
scoreboard_surface = pygame.Surface((SEGMENT_SIZE * 6, SEGMENT_SIZE * 16 + 10))  # with 10 pixel offset from top
scoreboard_pos = (center(play_surface_location[0], SEGMENT_SIZE * 6), play_surface_location[1])
scores = Score(("LEVEL:", "LINES:", "SCORE:"), [1, 0, -10], "gamedata")  # scoreboard initializes a Scoreboard object.
scores.get_highscore()  # retrieves previous highscore

"""
This segment contains variables/constants/objects used in the pause menu
________________________________________________________________________________________________________________________
"""
pause_surface_size = SEGMENT_SIZE * 9, SEGMENT_SIZE * 17
pause_surface = pygame.Surface(pause_surface_size, pygame.SRCALPHA)
pause_surface.set_alpha(125)
pause_surface_location = center(screen_width, pause_surface_size[0]), center(screen_height, pause_surface_size[1])
paused_text_surf = title_font.render("PAUSED", True, color_dict["white"])
paused_text_pos = center(screen_width, paused_text_surf.get_width()), 100
pause_button_left = center(screen_width, 288)
pause_button1 = TextButton(screen, (pause_button_left, 255, 288, 80), "RESUME", color_dict["dark gray"])
pause_button2 = TextButton(screen, (pause_button_left, 355, 288, 80), "HELP", color_dict["dark gray"])
pause_button3 = TextButton(screen, (pause_button_left, 455, 288, 80), "RESTART", color_dict["dark gray"])
pause_button4 = TextButton(screen, (pause_button_left, 555, 288, 80), "QUIT", color_dict["dark gray"])

"""
This segment contains variables/constants/objects used in the game over section.
________________________________________________________________________________________________________________________
"""
gameover_size = SEGMENT_SIZE * 20, SEGMENT_SIZE * 15
gameover_surface = pygame.Surface(gameover_size, pygame.SRCALPHA)
gameover_surface.set_alpha(125)
gameover_surface_location = center(screen_width, gameover_size[0]), center(screen_height, gameover_size[1])
score_box_rect = (gameover_surface_location[0] + SEGMENT_SIZE, gameover_surface_location[1] + SEGMENT_SIZE,
                  SEGMENT_SIZE * 11, gameover_size[1] - 2 * SEGMENT_SIZE)
gameover_button_left, gameover_button_top = score_box_rect[0] + score_box_rect[2] + SEGMENT_SIZE,\
                                              score_box_rect[1] + score_box_rect[3] - 275
gameover_button1 = TextButton(screen, (gameover_button_left, gameover_button_top, SEGMENT_SIZE * 6, 75),
                              "RESTART", color_dict["dark gray"])
gameover_button2 = TextButton(screen, (gameover_button_left, gameover_button_top + 100, SEGMENT_SIZE * 6, 75),
                              "MENU", color_dict["dark gray"])
gameover_button3 = TextButton(screen, (gameover_button_left, gameover_button_top + 200, SEGMENT_SIZE * 6, 75),
                              "EXIT", color_dict["dark gray"])
# GAME OVER message banner and location
game_text_surf = title_font.render("GAME", True, color_dict["white"])
over_text_surf = title_font.render("OVER!", True, color_dict["white"])
game_text_location = gameover_button_left, score_box_rect[1]
over_text_location = gameover_button_left, score_box_rect[1] + 75

"""
This segment contains variables/constants/objects used in the help and info section
________________________________________________________________________________________________________________________
"""
help_border_size = screen_width - 4 * SEGMENT_SIZE, screen_height - 4 * SEGMENT_SIZE
help_border = pygame.Surface(help_border_size)
help_border_location = center(screen_width, help_border_size[0]), center(screen_height, help_border_size[1])
help_text_surf = banner_font.render("HELP AND INFORMATION", True, (255, 255, 255))
help_text_pos = (center(screen_width, help_text_surf.get_width()), help_border_location[1] + 10)
with open("textbox", "r+") as hfile:  # h for help and info
    text = hfile.read()
info_box_rect = (help_border_location[0] + 20, help_border_location[1] + 60,
                 help_border_size[0] - 40, help_border_size[1] - 80)
info_box = TextBox(screen, text, info_box_rect)
back_button = TextButton(screen, (help_border_location[0] + SEGMENT_SIZE, help_border_location[1] + 10,
                                  4 * SEGMENT_SIZE, 40), "<< BACK", color_dict["darker gray"])
strt_button = TextButton(screen, ((help_border_location[0] + help_border_size[0] - 5 * SEGMENT_SIZE),
                                  help_border_location[1] + 10, 4 * SEGMENT_SIZE, 40),
                         "START >>", color_dict["darker gray"])

"""
Game state functions 
________________________________________________________________________________________________________________________
"""


def main_menu():  # function for the main menu
    clicked = False  # prevents inadvertent menu selections while holding mouse button down from other states
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # button interaction handled below, these are keyboard shortcuts
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # checks if user is holding modifying button
                    if event.key == pygame.K_g:
                        new_game()  # starts a new game
                        return "start"
                    elif event.key == pygame.K_h:
                        new_game()
                        return "help and info"
                    elif event.key == pygame.K_x:
                        running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        screen.blit(bg_img, (0, 0))
        screen.blit(title_surf, title_pos)
        screen.blit(copyrite_surf, copyrite_pos)

        if menu_button1.update_button() and clicked:  # displays start button and checks if user has clicked
            new_game()  # see event handler doc
            return "start"  # when user clicks button
        elif menu_button2.update_button() and clicked:
            new_game()
            return "help and info"
        elif menu_button3.update_button() and clicked:
            running = False  # ends game loop

        pygame.display.flip()
    return "exit"  # once game loop is ended and no game states are returned, program ends


def game_loop():  # main game loop functions
    global prev_shift_time, prev_drop_time, game_over, screen_capture, animation_count, \
        time_clicked_r, time_clicked_l, time_clicked_s
    running = True
    while running:
        clock.tick(60)
        if not game_over:
            """
            if dropped checks to see if the tetro has landed yet by comparing dropped to grace period (drop is
            incremented whenever the falling tetromino is blocked). If dropped does not equal or exceed grace period,
            the program checks for user input and updates positions. 
            """
            if dropped < grace_period:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False  # breaks running loop
                        game_over = True  # ends game
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # gets a copy of the screen for use in in the pause menu
                            screen_capture = pygame.Surface.copy(screen)
                            return "pause menu"
                        elif event.key == pygame.K_RIGHT:
                            """
                            The time_clicked_r variable is used to compare the time the right arrow key is pressed to
                            the duration of the user holding down the key. time_clicked_r as well as the other timing
                            variables below function as a delay for when the user holds down the direction keys.
                            """
                            time_clicked_r = pygame.time.get_ticks()
                            shift_right()  # moves tetro once without delay
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
                            hard_drop()  # instantly drops tetromino

                """
                Pygame's set_repeat function cannot be used here because some buttons do not have a hold down feature.
                Instead, this program uses Pygame's get_ticks to compare times and mimics the set_repeat feature.
                time_clicked tracks when the button was originally depressed. If enough time has elapsed, the tetromino
                can be shifted. Each shift also requires that enough time has passed from its last shift (so it does
                not instantly teleport pieces across the play surface).
                """
                # TODO: check if this segment can be simplified
                if pygame.time.get_ticks() - prev_drop_time >= drop_rate:  # enough time passed to drop tetro again
                    shift_down()
                    prev_drop_time = pygame.time.get_ticks()  # update last drop time

                pressed_keys = pygame.key.get_pressed()  # gets the state of all keys
                if pressed_keys[pygame.K_RIGHT]:  # checks if user has pressed the right arrow key
                    """
                    Checks if sufficient time has passed since the key was originally depressed and checks if enough 
                    time has passed the piece was last shifted. If conditions are met, the piece is shifted and 
                    the last shift time is updated.
                    """
                    # TODO: initialize time clicked variables
                    if (pygame.time.get_ticks() - time_clicked_r) >= KEY_DELAY \
                            and pygame.time.get_ticks() - prev_shift_time >= SHIFT_INTERVAL:
                        shift_right()
                        prev_shift_time = pygame.time.get_ticks()
                if pressed_keys[pygame.K_LEFT]:
                    if pygame.time.get_ticks() - time_clicked_l >= KEY_DELAY \
                            and pygame.time.get_ticks() - prev_shift_time >= SHIFT_INTERVAL:
                        shift_left()
                        prev_shift_time = pygame.time.get_ticks()
                if pressed_keys[pygame.K_s]:
                    if (pygame.time.get_ticks() - time_clicked_s) >= (KEY_DELAY - 100) \
                            and (pygame.time.get_ticks() - prev_drop_time) >= (SHIFT_INTERVAL - 26):
                        shift_down(5)  # Shift down is passed a 3 millisecond argument to extend the grace period
                        prev_drop_time = pygame.time.get_ticks()

                screen.blit(bg_img, (0, 0))
                update_play_surface()  # function handles surface and play surface
                display_next()  # display upcoming tetromino surface
                display_keys()  # display key instructions
                display_scoreboard()  # display scoreboard object
            else:
                """
                When dropped equals or exceeds grace period the a series of functions are called to generate a new
                piece, update scores, check for filled lines, etc.
                """
                check_pos()  # checks position of landed segments and assigns them to the correct group
                update_score()  # updates score attributes
                difficulty_level()  # increases difficulty when necessary

                # Creates a loop animation to destroy filled lines. User input is accepted during this loop.
                if get_lines():
                    animation_count = 0
                while animation_count < animation_length:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            animation_count = animation_length
                            running = False
                            game_over = True
                    line_animation()  # destroyed line animation for filled lines
                    animation_count += 1

                filled_lines_handler()  # empties filled rows and shifts other rows to their new position

                # creates a drop animation that still accepts user input
                while not rows_aligned() and running:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            game_over = True
                    shift_rows_down(9)

                new_tetro()  # generate a new tetro and new upcoming tetro
            pygame.display.flip()
        else:
            screen_capture = pygame.Surface.copy(screen)  # gets copy of current screen
            return "game over"
    return "exit"


def pause_menu():  # pause menu loop
    # TODO: create pause menu shortcuts
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "start"

        pause_surface.fill(color_dict["white"])
        screen.blit(screen_capture, (0, 0))
        screen.blit(pause_surface, (pause_surface_location[0], pause_surface_location[1]))
        screen.blit(paused_text_surf, paused_text_pos)
        if pause_button1.update_button():
            return "start"
        elif pause_button2.update_button():
            return "help and info"
        # TODO: double check if user wants to restart
        elif pause_button3.update_button():
            new_game()
            return "start"
        # TODO: double check if user wants to quit game
        elif pause_button4.update_button():
            return "main menu"
        pygame.display.flip()
    return "exit"


def gameover():  # game over loop
    # TODO: create gameover shortcuts
    if scores.highscore < scores.score_list[2]:  # checks if player has achieved new high score
        scores.set_highscore(scores.score_list[2])

    with open("gamedata", "r") as gfile:  # gfile for gameover file
        score_text = gfile.read()
    score_box = TextBox(screen, score_text, score_box_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    new_game()
                    return "start"
        gameover_surface.fill(color_dict["white"])
        screen.blit(screen_capture, (0, 0))
        screen.blit(gameover_surface, gameover_surface_location)
        score_box.update_box()
        if gameover_button1.update_button():
            new_game()
            return "start"
        if gameover_button2.update_button():
            return "main menu"
        if gameover_button3.update_button():
            return "exit"
        screen.blit(game_text_surf, game_text_location)
        screen.blit(over_text_surf, over_text_location)
        pygame.display.flip()
    return "exit"


def help_and_info():  # help and info state function
    screen.blit(bg_img, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    info_box.scroll(-5)
                elif event.button == 5:
                    info_box.scroll(5)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    info_box.text_top = 20
                    info_box.scroll_top = 20
                    return "main menu"
                elif event.key == pygame.K_DOWN:
                    info_box.scroll(12)
                elif event.key == pygame.K_UP:
                    info_box.scroll(-12)
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_g:
                        return "start"

        screen.blit(help_border, help_border_location)
        screen.blit(help_text_surf, help_text_pos)
        info_box.update_box()
        if back_button.update_button():
            info_box.text_top = 20  # resets text and scroll location on returning from menu
            info_box.scroll_top = 20
            return "main menu"
        elif strt_button.update_button():
            return "start"
        pygame.display.flip()
    return "exit"


"""
    This is the central loop that controls the state of the game. Each game state has a function (e.g. start game, 
game over, menu), and the game state is controlled by a return variable within each function.
    Once an event assigns a new game state to the game state variable, the function returns the game state and starts
a new function.
"""
game_state = "main menu"
# TODO: create loading state
# TODO: create ready state
while True:
    if game_state == "main menu":
        game_state = main_menu()
    elif game_state == "help and info":
        game_state = help_and_info()
    elif game_state == "start":
        game_state = game_loop()
    elif game_state == "pause menu":
        game_state = pause_menu()
    elif game_state == "game over":
        game_state = gameover()
    elif game_state == "exit":
        pygame.quit()
