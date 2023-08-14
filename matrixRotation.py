'''this code is a matrix rotation exercise. The code turns the matrix 90 degrees in a clockwise rotation.
works for the l_piece, j_piece, t_piece, s_piece, z_piece, i_piece, and o_piece.
the matrix is rotated by transposing the columns and rows and then reversing the rows.'''

import sys

def matrix_rotation():
    global matrix
    '''this code reformats the matrix list using a list comprehension expression. the list comprehension
    uses an outer loop to shift columns and an inner loop to move down the collumns.'''
    new_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    #all the rows are reversed
    for list in new_matrix:
        list.reverse()
    matrix = new_matrix
    for list in matrix:
        print(list)

#this is the position all tetrominos are originally displayed.
matrix = [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

new_matrix = []

for list in matrix:
    print(list)

#this code tests a full rotation to ensure the tetromino behaves as desired
for i in range(4):
    print()
    matrix_rotation()
