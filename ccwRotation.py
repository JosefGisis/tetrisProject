'''this code is a matrix rotation exercise. The code turns the matrix 90 degrees in a COUNTERclockwise rotation.
works for the l_piece, j_piece, t_piece, s_piece, z_piece, i_piece, and o_piece.
the matrix is rotated by transposing the rows and columns and then reverses the order of the rows.'''

import sys

def ccw_rotation():
    global matrix
    """this list comprehension expression switches the rows for columns and reverses the order of rows"""
    new_matrix = [[matrix[j][i] for j in range(len(matrix[0]))] for i in range(len(matrix))]
    #order of rows are reversed
    new_matrix.reverse()
    matrix = new_matrix
    for list in matrix:
        print(list)

#this is the position all tetrominos are originally displayed.
matrix = [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]]

new_matrix = []

for list in matrix:
    print(list)

#this code tests a full rotation to ensure the tetromino behaves as desired
for i in range(4):
    print()
    ccw_rotation()
