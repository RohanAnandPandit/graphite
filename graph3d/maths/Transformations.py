from math import sin, cos, radians

# See documentation for how these matrices work
def rotation(angle, axis):
    angle = radians(angle) # Angles have to be in radians
    (sine, cosine) = (sin(angle), cos(angle))
    if (axis == 'x'):
        matrix = [[1,      0,      0, 0],
                  [0, cosine,  -sine, 0],
                  [0,   sine, cosine, 0],
                  [0,      0,      0, 1]]

    elif (axis == 'y'):
        matrix = [[ cosine, 0,   sine, 0],
                  [      0, 1,      0, 0],
                  [  -sine, 0, cosine, 0],
                  [          0, 0,  0, 1]]
    elif (axis == 'z'):
        matrix = [[cosine,  -sine, 0, 0],
                  [  sine, cosine, 0, 0],
                  [     0,      0, 1, 0],
                  [     0,      0, 0, 1]]
    return matrix

def rotationAboutLine(angle, line):
    angle = radians(angle)
    # Components of direction vector of line
    u = line.point2.cor[0] - line.point1.cor[0]
    v = line.point2.cor[1] - line.point1.cor[1]
    w = line.point2.cor[2] - line.point1.cor[2]

    magnitude = mag([u,v,w])
    #Unit direction vector
    u = u / magnitude
    v = v / magnitude
    w = w / magnitude

    # Coordinates of a point that line passes through
    a = line.point1.cor[0]
    b = line.point1.cor[1]
    c = line.point1.cor[2]

    (sine, cosine) = (sin(angle), cos(angle))
    return [[cosine+u*u*(1-cosine), u*v*(1-cosine)-w*sine, u*w*(1-cosine)+v*sine, (a*(v**2+w**2)-u*(b*v+c*w))*(1-cosine)+(-c*v+b*w)*sine],
            [u*v*(1-cosine)+w*sine, cosine+v*v*(1-cosine), v*w*(1-cosine)-u*sine, (b*(u**2+w**2)-v*(a*u+c*w))*(1-cosine)+(c*u-a*w)*sine],
            [u*w*(1-cosine)-v*sine, v*w*(1-cosine)+u*sine,cosine+w*w*(1-cosine),(c*(u**2+v**2)-w*(a*u+b*v))*(1-cosine)+(-b*u+a*v)*sine],
            [0,0,0,1]]


def reflection(plane):
    if (plane=='x'):
        matrix = [[-1, 0, 0, 0],
                  [ 0, 1, 0, 0],
                  [ 0, 0, 1, 0],
                  [ 0, 0, 0, 1]]
    if (plane == 'y'):
        matrix = [[1,  0, 0, 0],
                  [0, -1, 0, 0],
                  [0,  0, 1, 0],
                  [0,  0, 0, 1]]
    if (plane=='z'):
        matrix = [[1, 0,  0, 0],
                  [0, 1,  0, 0],
                  [0, 0, -1, 0],
                  [0, 0,  0, 1]]
    return matrix

def scale(xSf = 1, ySf = 1, zSf = 1):
    matrix = [[xSf,   0,   0, 0],
              [  0, ySf,   0, 0],
              [  0,   0, zSf, 0],
              [  0,   0,   0, 1]]
    return matrix

def translation(x,y,z):
    matrix = [[1, 0, 0, x],
              [0, 1, 0, y],
              [0, 0, 1, z],
              [0, 0, 0, 1]]
    return matrix
