from math import sin, cos, radians, sqrt


def mag(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2)


# See documentation for how these matrices work
def rotation(angle, axis):
    angle = radians(angle)  # Angles have to be in radians
    (sine, cosine) = (sin(angle), cos(angle))

    if axis == 'x':
        matrix = [[1, 0, 0, 0],
                  [0, cosine, -sine, 0],
                  [0, sine, cosine, 0],
                  [0, 0, 0, 1]]

    elif axis == 'y':
        matrix = [[cosine, 0, sine, 0],
                  [0, 1, 0, 0],
                  [-sine, 0, cosine, 0],
                  [0, 0, 0, 1]]

    elif axis == 'z':
        matrix = [[cosine, -sine, 0, 0],
                  [sine, cosine, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]

    return matrix


def rotation_about_line(angle, line):
    u = line.point2.cor[0] - line.point1.cor[0]
    v = line.point2.cor[1] - line.point1.cor[1]
    w = line.point2.cor[2] - line.point1.cor[2]

    a = line.point1.cor[0]
    b = line.point1.cor[1]
    c = line.point1.cor[2]

    return rotation_about_vector(angle, (a, b, c), (u, v, w))


def rotation_about_vector(angle, point, vector):
    angle = radians(angle)
    # Components of direction vector of line
    u, v, w = vector
    a, b, c = point
    magnitude = mag(u, v, w)
    # Unit direction vector
    u = u / magnitude
    v = v / magnitude
    w = w / magnitude

    # Coordinates of a point that line passes through

    (sine, cosine) = (sin(angle), cos(angle))
    uv = u ** 2 + v ** 2
    uw = u ** 2 + w ** 2
    vw = v ** 2 + w ** 2
    p = 1 - cosine
    return [[cosine + u * u * p, u * v * p - w * sine, u * w * p + v * sine,
             (a * vw - u * (b * v + c * w)) * p + (-c * v + b * w) * sine],

            [u * v * p + w * sine, cosine + v * v * p, v * w * p - u * sine,
             (b * uw - v * (a * u + c * w)) * p + (c * u - a * w) * sine],

            [u * w * p - v * sine, v * w * p + u * sine, cosine + w * w * p,
             (c * uv - w * (a * u + b * v)) * p + (-b * u + a * v) * sine],

            [0, 0, 0, 1]]


def reflection(plane):
    if plane == 'x':
        matrix = [[-1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]
    if plane == 'y':
        matrix = [[1, 0, 0, 0],
                  [0, -1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]
    if plane == 'z':
        matrix = [[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, -1, 0],
                  [0, 0, 0, 1]]

    return matrix


def scale(xSf=1, ySf=1, zSf=1):
    return [[xSf, 0, 0, 0],
            [0, ySf, 0, 0],
            [0, 0, zSf, 0],
            [0, 0, 0, 1]]


def translation(x, y, z):
    return [[1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]]
