"""this code is practice for tetromino objects, functions, and attributes. many details may change when
implemented into a functional program."""

import sys, pygame, random

'''all tetromino shapes are drawn on a square matrix. shapes are constructed with a matrix so that 
they can be rotated. in this code, the location of the squares are designated by the numbers in the 
matrices (numbers three to six). This method will likely need to change later to only ones and zeros, 
and the locations will be set through a for loop'''
#the i piece needs to have a grid 4x4 to allow rotation
i_piece = [[0, 0, 0, 0],
           [3, 4, 5, 6],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

j_piece = [[3, 0, 0],
           [3, 4, 5],
           [0, 0, 0]]

l_piece = [[0, 0, 5],
           [3, 4, 5],
           [0, 0, 0]]

t_piece = [[0, 4, 0],
           [3, 4, 5],
           [0, 0, 0]]

o_piece = [[4, 5],
           [4, 5]]

s_piece = [[0, 4, 5],
           [3, 4, 0],
           [0, 0, 0]]

z_piece = [[3, 4, 0],
           [0, 4, 5],
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
    global y
    for row in current_letter:
        for column in row:
            #checks to see if there is a number
            if column >= 3:
                #this uses the numbers in the matrix to get the location
                x = 32 * column
                #initializes a new square for the tetromino
                new_square = Square([x, y], color)
                #adds the new square to a group object that makes up the tetrominos
                current_piece.add(new_square)
        y += 32

def shift_right():
    global current_piece, rightmost
    #checks if the piece has hit the bottom yet
    if moving == True:
        #checks if the tetromino has hit the right wall
        for piece in current_piece.sprites():
            if piece.rect.right >= 298:
                rightmost = True
        if rightmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx += 32

def shift_left():
    global current_piece, leftmost
    if moving == True:
        #checks if the tetromino has hit the left wall;
        for piece in current_piece.sprites():
            if piece.rect.left <= 0:
                leftmost = True
        if leftmost == False:
            for piece in current_piece.sprites():
                piece.rect.centerx -= 32

def shift_down():
    global current_piece, moving
    #checks if the tetromino has hit the bottom
    for piece in current_piece.sprites():
        if piece.rect.bottom >= 636:
            #when the tetromino has hit the bottom it is no longer moving and disables and horizontal movement
            moving = False
    if moving == True:
        for piece in current_piece.sprites():
            piece.rect.centery += 32


pygame.init()
screen = pygame.display.set_mode([318, 638])
clock = pygame.time.Clock()
screen.fill([0, 0, 0])
#this sprite group holds the current tetromino
current_piece = pygame.sprite.Group()
#y is initialize to start off the top of the play surface
y = -64
moving = True
leftmost = False
rightmost = False

running = True

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
gen_piece(green)
#pygame event to make the piece descend
pygame.time.set_timer(25, 500)


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
            #this is a temporary event for testing and will be removed later
            elif event.key == pygame.K_UP:
                for piece in current_piece.sprites():
                    piece.rect.centery -= 32
                moving = True
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

