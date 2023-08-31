import sys, pygame, random

class Square(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = green_segment
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

current_piece = pygame.sprite.Group()
def gen_piece():
    global starty, startx
    current_piece.empty()
    for row in range(len(current_letter)):
        for column in range(len(current_letter)):
            if current_letter[row][column] == 1:
                x = startx + (square_size * column)
                y = starty + (square_size * row)
                new_square = Square([x, y])
                current_piece.add(new_square)

dropped_segments = pygame.sprite.Group()
def update_surface():
    global starty, startx, current_piece, current_letter, moving
    for piece in current_piece.sprites():
        dropped_segments.add(piece)
    current_piece.empty()
    starty = (-2 * square_size)
    startx = (3 * square_size)
    current_letter = random.choice(tetro_list)
    gen_piece()
    moving = True
def shift_right():
    global current_piece, rightmost, startx
    if moving == True:
        for piece in current_piece.sprites():
            if piece.rect.right >= play_surface_width:
                rightmost = True
        if rightmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx += square_size
            startx += square_size

def shift_left():
    global current_piece, leftmost, startx
    if moving == True:
        for piece in current_piece.sprites():
            if piece.rect.left <= 0:
                leftmost = True
        if leftmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx -= square_size
            startx -= square_size

def shift_down():
    global current_piece, moving, starty
    for piece in current_piece.sprites():
        if piece.rect.bottom >= play_surface_height:
            moving = False
    if moving == True:
        for piece in current_piece.sprites():
            piece.rect.centery += square_size
        starty += square_size

def rotate_tetro():
    global current_letter, O
    if current_letter != O and moving:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))] for i in range(len(current_letter[0]))]
        for list in rotated_letter:
            list.reverse()
        current_letter = rotated_letter

def ccw_tetro():
    global current_letter, O
    if current_letter != O and moving:
        ccw_letter = [[current_letter[j][i] for j in range (len(current_letter[0]))] for i in range(len(current_letter))]
        ccw_letter.reverse()
        current_letter = ccw_letter

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
square_size = 36
starty = (-2 * square_size)
startx = (3 * square_size)
moving = True
leftmost = False
rightmost = False
USEREVENT = 25

pygame.init()
display_size = screen_width, screen_height = (1000, 800)
screen = pygame.display.set_mode(display_size)
play_surface_size = (play_surface_width, play_surface_height) = ((square_size * 10), (square_size * 20))
pygame.display.set_caption("TITLE PLACEHOLDER")
pygame.time.Clock()
bg_img = pygame.transform.scale(pygame.image.load("bg.jpg"), display_size)
green_segment = pygame.image.load("green_segment.jpeg")
pygame.time.set_timer(USEREVENT, 1000)
current_letter = random.choice(tetro_list)
gen_piece()
def start_game():
    global rightmost, leftmost
    running = True
    while running:
        if moving:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        shift_right()
                        leftmost = False
                    elif event.key == pygame.K_LEFT:
                        shift_left()
                        rightmost = False
                    elif event.key == pygame.K_d:
                        rotate_tetro()
                        gen_piece()
                    elif event.key == pygame.K_a:
                        ccw_tetro()
                        gen_piece()
                elif event.type == USEREVENT:
                    shift_down()

            screen.blit(bg_img, (0, 0))
            play_surface = pygame.Surface((play_surface_size))
            current_piece.draw(play_surface)
            dropped_segments.draw(play_surface)
            screen.blit(play_surface, (((screen_width - play_surface_width) // 2),
                                           ((screen_height - play_surface_height) // 2)))

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            update_surface()
    pygame.quit()

start_game()

