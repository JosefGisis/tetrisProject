This is the code for my first official Python project. It is a bare-bones tetris style game.
- Josef Gisis 9/8/2023

This game is currently at version 1.4. Future versions will contain improved graphics, and tetrominos will be 
contained within classes, as well as many other features.

![Alt Text](tetris-menu-_1_.gif)

click here for full video: https://youtu.be/pJ7ecHluLM8

or here for extended gameplay: https://youtu.be/H3VQvaIEuHo

Surface images for tetris pieces and destroyed lines created by Josef Gisis

Background image designed by rawpixel.com / Freepik


ADDITIONAL DOCUMENTATION:

    Information on tetromino rotation functions (see program documentation first):

    Both the clockwise and counterclockwise rotation functions use list comprehension methods to rotate the tetrominos
    ninety degrees at a time. Each tetromino is represented by a letter constant (L_piece, O_PIECE, S_PIECE, Z_PIECE,
    T_PIECE, J_PIECE, and L_PIECE) assigned by a list array (matrix).

    In order to rotate each matrix we can use a list comprehension method to transpose the rows and columns of each
    matrix. For example:
    The tetromino S   [0, 1, 1]    rotates clockwise to    [0, 1, 0]    and counterclockwise to    [1, 0, 0]
                      [1, 1, 0]                            [0, 1, 1]                               [1, 1, 0]
                      [0, 0, 0]                            [0, 0, 1]                               [0, 1, 0]

    Note that when the S pieces is rotated clockwise, the top row become the last column, the middle row becomes the the
    middle column, and the bottom row becomes of the first column. We can use an algorithm to take the contents of each
    row and displays them vertically in ascending order and then reverses the order of each row.

    For example:   [0, 1, 1]   to   [0, 1, 0]   to   [0, 1, 0]   by reversing each row in the second matrix.
                   [1, 1, 0]        [1, 1, 0]        [0, 1, 1]
                   [0, 0, 0]        [1, 0, 0]        [0, 0, 1]

    The code may go something like this (using Python).

    matrix = [[0, 1, 0],
              [1, 1, 0],
              [0, 0, 0]]

    for row in matrix:
        print(row)

    new_matrix = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            new_matrix[column][row] = matrix[row][column]
    for row in new_matrix:
        row.reverse()

    print()
    for row in new_matrix:
        print(row)

    This is a very basic idea of the logic. The reader may note: in order to rotate this matrix counterclockwise, rather
    than reverse the order of each row, reverse the list itself (or put differently, reverse the order of the columns).
    The reader may take the above code, and see how it behaves with different shapes and with grids of different sizes.

    Python offers a very powerful and quick list comprehension method that goes as such:

    new_list = [perform x expression >>> for objects in old_list >>> while x condition is met]

    We can use list comprehension to rotate matrices:

    matrix = [[0, 1, 0],
              [1, 1, 0],
              [0, 0, 0]]

    for row in matrix:
        print(row)

    new_matrix = [[matrix[column][row] for column in range(len(matrix[row]))] for row in range(len(matrix))]
    for row in new_matrix:
        row.reverse()

    print()
    for row in new_matrix:
        print(row)

    The tetris game does not just display matrices; rather, a generate piece function creates segment objects by
    checking the contents of the matrix. When a tetromino is flipped a rotate function is called that takes the current
    matrix in use, say L, and rotates the matrix. Then a new tetromino is creates by generating a new piece using the
    rotated matrix. In the program the code looks like this:

    def cw_rotation():
    global current_letter, rotation_state, startx, starty
    blocked = False
    if current_letter != O_PIECE and moving < delay:
        rotated_letter = [[current_letter[j][i] for j in range(len(current_letter))]
                          for i in range(len(current_letter[0]))]
        for list in rotated_letter:
            list.reverse()
        gen_tetro(rotated_letter, current_surface)

    After each tetromino is rotated, the function checks if the piece has collided with other dropped segments. If it
    has, each tetromino is tested in multiple location and set in the first available space. If all spaces are taken
    the rotation is cancelled. Here is the full clockwise rotation function:

    def cw_rotation():
    global current_letter, rotation_state, startx, starty
    blocked = False
    if current_letter != O_PIECE and moving < delay:
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

    Note: many of the global variables would be better handled as class attributes; however, because each square is part
    of the Square class (see program), the tetrominos need to be manipulated through a sprite group.

    The first test is done after the first rotation. If the tetromino is blocked, the function first checks if the
    current tetromino is the I piece. This is because the I piece is tested differently due to its length. Then the
    function checks the rotation state. Rotation state refers to the degree of rotation of each piece (0, 90, 180, and
    270). Depending on the degree of rotation, different tests are performed because certain collisions are more likely
    to occur at different angles of rotation. Furthermore, depending if the piece is rotating clockwise or
    counterclockwise, different test are performed. Because this is the clockwise rotation function, we only need to
    check for ascending degrees of rotation (e.g. 0 to 90 or 270 to 0). These degrees of rotation are referred to as 0
    for 0 degrees, 1 for 90 degrees, 2 for 180 degrees, etc.

    The i variable controls the current rotation state and applies the correct tests. The j variable iterates through
    all the tests. The function finds the rotational state through the i variable, and iterates through a list of test
    moves to find the first available spot (eg. cw_check[i][j][0]). If a spot is found, blocked is set to False and the
    rotational state is updated. If no spot is available, the tetromino is set back to its original position (found at
    the last location in the test move list) and a non rotated piece is regenerated (that is the rotation is cancelled).

    There are several options to set the test location. The first is to use the official Tetris guidelines, the Super
    Rotation System.

    Test moves for the s, z, t, l, and j pieces:

            Test 1	Test 2	Test 3	Test 4	Test 5
    0 >> 1	(0, 0)	(-1, 0)	(-1, 1)	(0,-2)	(-1,-2)
    1 >> 0	(0, 0)	(1, 0)	(1,-1)	(0, 2)	(1, 2)
    1 >> 2	(0, 0)	(1, 0)	(1,-1)	(0, 2)	(1, 2)
    2 >> 1	(0, 0)	(-1, 0)	(-1, 1)	(0,-2)	(-1,-2)
    2 >> 3	(0, 0)	(1, 0)	(1, 1)	(0,-2)	(1,-2)
    3 >> 2	(0, 0)	(-1, 0)	(-1,-1)	(0, 2)	(-1, 2)
    3 >> 0	(0, 0)	(-1, 0)	(-1,-1)	(0, 2)	(-1, 2)
    0 >> 3	(0, 0)	(1, 0)	(1, 1)	(0,-2)	(1,-2)

    Test moves for the i piece:

            Test 1	Test 2	Test 3	Test 4	Test 5
    0 >> 1	(0, 0)	(-2, 0)	(1, 0)	(-2,-1)	(1, 2)
    1 >> 0	(0, 0)	(2, 0)	(-1, 0)	(2, 1)	(-1,-2)
    1 >> 2	(0, 0)	(-1, 0)	(2, 0)	(-1, 2)	(2,-1)
    2 >> 1	(0, 0)	(1, 0)	(-2, 0)	(1,-2)	(-2, 1)
    2 >> 3	(0, 0)	(2, 0)	(-1, 0)	(2, 1)	(-1,-2)
    3 >> 2	(0, 0)	(-2, 0)	(1, 0)	(-2,-1)	(1, 2)
    3 >> 0	(0, 0)	(1, 0)	(-2, 0)	(1,-2)	(-2, 1)
    0 >> 3	(0, 0)	(-1, 0)	(2, 0)	(-1, 2)	(2, -1)

    The numbers refers to x and y movements (e.g. 1 means one horizontal shift to the right). Each move is relative to
    the tetrominos original location. In order to undo each prior test the list needs to be modified.

    Here are four lists for clockwise rotations, counterclockwise rotations, clockwise rotations for i piece, and
    counterclockwise rotations for i piece. The last entry for each sublist is for returning the piece to its original
    location if it fails rotation.

    cw_check = [[[-1, 0], [0, 1], [1, -3], [-1, 0], [1, 2]], [[1, 0], [0, -1], [-1, 3], [1, 0], [-1, -2]],
                [[1, 0], [0, 1], [-1, -3], [1, 0], [-1, 2]], [[-1, 0], [0, -1], [1, 3], [-1, 0], [1, -2]]]

    cw_lpiece_check = [[[-2, 0], [3, 0], [-3, -1], [3, 3], [-1, -2]], [[-1, 0], [3, 0], [-3, 2], [3, -3], [-2, 1]],
                       [[2, 0], [-3, 0], [3, 1], [-3, -3], [1, 2]], [[1, 0], [-3, 0], [3, -2], [-3, 3], [2, -1]]]

    ccw_check = [[[1, 0], [0, 1], [-1, -3], [1, 0], [-1, 2]], [[1, 0], [0, -1], [-1, 3], [1, 0], [-1, -2]],
                 [[-1, 0], [0, 1], [1, -3], [-1, 0], [1, 2]], [[-1, 0], [0, -1], [1, 3], [-1, 0], [1, -2]]]

    ccw_lpiece_check = [[[-1, 0], [3, 0], [-3, 2], [3, -3], [-2, 1]], [[2, 0], [-3, 0], [3, 1], [-3, -3], [1, 2]],
                        [[1, 0], [-3, 0], [3, -2], [-3, 3], [2, -1]], [[-2, 0], [3, 0], [-3, -1], [3, 3], [-1, -2]]]

    The issue with these lists is that when they are implemented, tetrominos bounced of the bottom of the floor of the
    play surface shift left or right (they do not spin in place). Here is an altered list:

    cw_check = [[[0, 1], [-1, 0], [1, -3], [-1, 0], [1, 2]], [[1, 0], [0, -1], [-1, 3], [1, 0], [-1, -2]],
            [[1, 0], [0, 1], [-1, -3], [1, 0], [-1, 2]], [[-1, 0], [0, -1], [1, 3], [-1, 0], [1, -2]]]

    cw_ipiece_check = [[[0, 2], [1, -2], [-3, -1], [3, 3], [-1, -2]], [[-1, 0], [3, 0], [-3, 2], [3, -3], [-2, 1]],
                       [[2, 0], [-3, 0], [3, 1], [-3, -3], [1, 2]], [[1, 0], [-3, 0], [3, -2], [-3, 3], [2, -1]]]

    ccw_check = [[[0, 1], [1, 0], [-1, -3], [1, 0], [-1, 2]], [[1, 0], [0, -1], [-1, 3], [1, 0], [-1, -2]],
                 [[-1, 0], [0, 1], [1, -3], [-1, 0], [1, 2]], [[-1, 0], [0, -1], [1, 3], [-1, 0], [1, -2]]]

    ccw_ipiece_check = [[[0, 2], [-1, -2], [0, 2], [3, -3], [-2, 1]], [[2, 0], [-3, 0], [3, 1], [-3, -3], [1, 2]],
                        [[1, 0], [-3, 0], [3, -2], [-3, 3], [2, -1]], [[-2, 0], [3, 0], [-3, -1], [3, 3], [-1, -2]]]

    Note the changes in the first list in each list.

    Or a simpler version:

    cw_check = [[[0, 1], [-1, -1], [2, 0], [-1, -1], [0, 1]], [[1, 0], [-1, 1], [0, -2], [-1, 1], [1, 0]],
                [[0, -1], [1, 1], [-2, 0], [1, 1], [0, -1]], [[-1, 0], [1, -1], [0, 2], [1, -1], [-1, 0]]]

    cw_ipiece_check = [[[0, 2], [0, -3], [-2, 1], [3, 0], [-1, 0]], [[2, 0], [-3, 0], [1, 2], [0, -3], [0, 1]],
                       [[0, -2], [0, 3], [2, -1], [-3, 0], [1, 0]], [[-2, 0], [3, 0], [-1, -2], [0, 3], [0, -1]]]

    ccw_check = [[[0, 1], [1, -1], [-2, 0], [1, -1], [0, 1]], [[1, 0], [-1, -1], [0, 2], [-1, -1], [1, 0]],
                 [[0, -1], [-1, 1], [2, 0], [-1, 1], [0, -1]], [[-1, 0], [1, 1], [0, -2], [1, 1], [-1 ,0]]]

    ccw_ipiece_check = [[[0, 2], [0, -3], [2, 1], [-3, 0], [1, 0]], [[2, 0], [-3, 0], [1, -2], [0, 3], [0, -1]],
                        [[0, -2], [0, 3], [-2, -1], [3, 0], [-1, 0]], [[-2, 0], [3, 0], [-1, 2], [0, -3], [0, 1]]]

    Lighter versions are also possible. For example, except for the i piece, all tetrominos can have a uniform test of
    testing all four non-diagonal adjacent spots (0, 1): right, (0, -1): down, (-1, 0): left, and (0, 1): up. Althout it
    is not the fastest, this method can be used regardless of angle of rotation and whether it is being rotated
    clockwise or counterclockwise. I piece would have to be tested 2 right, 1 down, 2 left, 1 up, 1 right, 2 down,
    1 left, and 2 up. The upside to this method would be that it would require fewer conditions, but the downside would
    be that it would require more tests for every piece.

    Continued testing is required to find the optimal rotation tests.

    In summary, each tetromino is displayed using a letter matrix. When the user rotates the tetromino, one the rotation
    function uses a list comprehension method to rotate the letter. Then a new tetromino is generated using the rotated
    list. The rotated piece is then checked if it is blocked. If the piece is blocked then depending on the kind of tet-
    romino, the degree of rotation, and depending if it is being rotated clockwise or counterclockwise a series of test
    locations are applied to see which is the first one available. If none of the locations are available, the piece is
    returned to its original location and the rotation is cancelled.
