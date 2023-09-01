"""this code implements matrix rotation to all tetromino pieces"""

import sys, pygame, random

'''all tetromino shapes are drawn on a square matrix. shapes are constructed with a matrix so that 
they can be rotated. in this code, the location of the squares are designated by the numbers in the 
matrices (numbers three to six). This method will likely need to change later to only ones and zeros, 
and the locations will be set through a for loop'''

#the i piece needs to have a grid 4x4 to allow rotation
i_piece = [[0, 0, 0, 0],
           [1, 1, 1, 1],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

j_piece = [[1, 0, 0],
           [1, 1, 1],
           [0, 0, 0]]

l_piece = [[0, 0, 1],
           [1, 1, 1],
           [0, 0, 0]]

t_piece = [[0, 1, 0],
           [1, 1, 1],
           [0, 0, 0]]

o_piece = [[0, 1, 1],
           [0, 1, 1],
           [0, 0, 0]]

s_piece = [[0, 1, 1],
           [1, 1, 0],
           [0, 0, 0]]

z_piece = [[1, 1, 0],
           [0, 1, 1],
           [0, 0, 0]]

#shapes need to be placed in list before using the shape function
shape_list = [i_piece, j_piece, i_piece, t_piece, o_piece, s_piece, z_piece]

current_letter = random.choice(shape_list)

#this class creates the individual blocks for each tetromino
class Square(pygame.sprite.Sprite):
    def __init__(self, location, color):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([30, 30])
        image_surface.fill(color)
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

#this function generates each tetromino
def gen_piece(color):
    #startx and y control where the tetrominos start
    global starty, startx
    current_piece.empty()
    for row in range(len(current_letter)):
        y = starty + (row * 32)
        #gets the length of each list within current_letter. This iterates the squares and tests if there is a 1
        for column in range(len(current_letter)):
            #checks to see if a square should be placed in that grid
            if current_letter[row][column] == 1:
                #this uses the for loop and startx to display the piece
                x = startx + (32 * column)
                #initializes a new square for the tetromino
                new_square = Square([x, y], color)
                #adds the new square to a group object that makes up the tetrominos
                current_piece.add(new_square)

def shift_right():
    global current_piece, rightmost, startx
    #checks if the piece has hit the bottom yet
    if moving == True:
        #checks if the tetromino has hit the right wall
        for piece in current_piece.sprites():
            if piece.rect.right >= 298:
                rightmost = True
        if rightmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx += 32
            startx += 32

def shift_left():
    global current_piece, leftmost, startx
    if moving == True:
        #checks if the tetromino has hit the left wall;
        for piece in current_piece.sprites():
            if piece.rect.left <= 0:
                leftmost = True
        if leftmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx -= 32
            startx -= 32

def shift_down():
    global current_piece, moving, starty
    #checks if the tetromino has hit the bottom
    for piece in current_piece.sprites():
        if piece.rect.bottom >= 636:
            #when the tetromino has hit the bottom it is no longer moving and disables and horizontal movement
            moving = False
    if moving == True:
        for piece in current_piece.sprites():
            piece.rect.centery += 32
        starty += 32

def rotate_tetro():
    global current_letter, o_piece
    if current_letter != o_piece and moving:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))] for i in range(len(current_letter[0]))]
        # all the rows are reversed
        for list in rotated_letter:
            list.reverse()
        current_letter = rotated_letter

def ccw_tetro():
    global current_letter, o_piece
    if current_letter != o_piece and moving:
        ccw_letter = [[current_letter[j][i] for j in range (len(current_letter[0]))] for i in range(len(current_letter))]
        #order of rows are reversed
        ccw_letter.reverse()
        current_letter = ccw_letter

pygame.init()
screen = pygame.display.set_mode([318, 638])
clock = pygame.time.Clock()
screen.fill([255, 255, 255])
#this sprite group holds the current tetromino
current_piece = pygame.sprite.Group()
#y is initialize to start off the top of the play surface
starty = -64
startx = 96
moving = True
leftmost = False
rightmost = False

'''I should add this to a dictionary. or I can create a dictionary containing the
shapes as keys and the colors as values'''
purple = [208, 48, 217]
red = [227, 11, 33]
teal = [13, 209, 180]
blue = [14, 97, 240]
green = [8, 199, 24]
magenta = [199, 8, 126]
coral = [255, 127, 80]


'''later in development, each piece will be assigned one of the prior colors. this 
is not how tetrominos will be called, so all pieces are generated with the same color'''
gen_piece(red)
#pygame event to make the piece descend
pygame.time.set_timer(25, 1000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                shift_right()
                #when the user moves right, the tetromino is no longer leftmost
                leftmost = False
            elif event.key == pygame.K_LEFT:
                shift_left()
                #when the user moves left, the tetromino is no longer rightmost
                rightmost = False
            elif event.key == pygame.K_d:
                rotate_tetro()
                gen_piece(red)
            elif event.key == pygame.K_a:
                ccw_tetro()
                gen_piece(red)
        elif event.type == 25:
            shift_down()
    '''this code below is temporary and will not be active later. this code creates
    a grid to help development'''
    for i in range(10):
        for j in range(20):
            x = i * 32
            y = j * 32
            pygame.draw.rect(screen, [0, 0, 0], [x, y, 30, 30], 0)
    #this is a group method that draws all the squares in the current tetromino
    current_piece.draw(screen)

    pygame.display.flip()

pygame.quit()

