# For more informaion about why these functions are required and how they work,
# see the 'Algorithms' section of the doumentation
from math import sqrt

def create_matrix(rows, columns):
    matrix = []
    row = []
    for i in range(columns):
        row.append(0)
    for j in range(rows):
        matrix.append(row.copy())
    return matrix


# Calculates the dot product of two vectors
def dot(v1, v2):
    if len(v1) != len(v2):
        print("Cannot calculate dot product")
        return
    sum = 0
    for i in range(0, len(v1)):
        sum += v1[i] * v2[i]
    return sum


# Multiplies the transformation matrix by the point's position vector and
# returns the new coordinates
def transform(posVec, transfMatrix):
    image = []
    for row in transfMatrix:
        image.append(dot(posVec, row))
    image += [1]
    return image


# Gets nth column by iterating through each row of the 2nd matrix
def get_column(matrix, columnNum):
    column = []
    for row in range(0, len(matrix)):
        column.append(matrix[row][columnNum])
    return column


# Multiplies any two valid matrices
def matrix_multiply(m1, m2):
    if len(m1[0]) != len(m2):
        print("Cannot multiply matrices")

    (rows, columns) = (len(m1[0]), len(m2[0]))
    mat_prod = create_matrix(rows, columns)
    for row in range(len(m1)):  # Iterates through each row of 1st matrix
        # Iterates through all the columns of 2nd matrix
        for column_number in range(len(m2[0])):
            column = get_column(m2, column_number)
            element = dot(m1[row], column)  # value of element in row and column number
            mat_prod[row][column_number] = element

    return mat_prod


# Adds two 3-dimensional vectors
def add(m1, m2):
    if len(m1) != len(m2):
        print("Cannot add matrices")
        return
    if len(m1) != 0:
        if len(m1[0]) != len(m2[0]):
            print("Cannot add matrices")
            return

    (rows, columns) = (len(m1), len(m1[0]))
    sum_matrix = create_matrix(rows, columns)
    for j in range(rows):
        for i in range(columns):
            sum_matrix[j][i] = m1[j][i] + m2[j][i]
    return sum_matrix


def cross(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print("Cannot calculate cross product")

    (x1, y1, z1) = v1
    (x2, y2, z2) = v2

    i = y1 * z2 - z1 * y2
    j = -(x1 * z2 - z1 * x2)
    k = x1 * y2 - y1 * x2
    return i, j, k


def mag(vector):
    sum = 0
    for i in range(0, len(vector)):
        sum += vector[i] ** 2

    return sqrt(sum)
