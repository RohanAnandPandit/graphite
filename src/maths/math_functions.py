# Certain mathematical functions are not defined within the math library of Python
# or not represented in the way people typically write the functions.
# Therefore by defining the following functions the in-built eval() function will
# be able to evaluate expressions inputted by the user which use these functions
# for e.g. ln(y) = arcsin(x)


from math import *


def ln(x):
    return log(x, e)


def cosec(x):
    return 1 / sin(x)


def sec(x):
    return 1 / cos(x)


def cot(x):
    return 1 / tan(x)


def cosech(x):
    return 1 / sinh(x)


def sech(x):
    return 1 / cosh(x)


def coth(x):
    return 1 / tanh(x)


def arcsin(x):
    return asin(x)


def arcos(x):
    return acos(x)


def arccos(x):
    return acos(x)


def arctan(x):
    return atan(x)


def acosec(x):
    return asin(1 / x)


def asec(x):
    return acos(1 / x)


def acot(x):
    return atan(1 / x)


def acosech(x):
    return asinh(1 / x)


def asech(x):
    return acosh(1 / x)


def acoth(x):
    return atanh(1 / x)


def arcosec(x):
    return asin(1 / x)


def arccosec(x):
    return asin(1 / x)


def arcsec(x):
    return acos(1 / x)


def arccot(x):
    return atan(1 / x)


def arcot(x):
    return atan(1 / x)


def arcosech(x):
    return asinh(1 / x)


def arccosech(x):
    return asinh(1 / x)


def arcsech(x):
    return acosh(1 / x)


def arcoth(x):
    return atanh(1 / x)


def arccoth(x):
    return atanh(1 / x)


def fact(x):
    return factorial(x)


def sigma(start, end, expression, step=1):
    from ..string_formatting import syntax_correction
    sum = 0
    r = start
    expression = syntax_correction(expression)
    while r <= end:
        sum += eval(expression)
        r += step

    return sum


def mag_complex(number):
    return sqrt((number.real ** 2) + (number.imag ** 2))


def mandelbrot(x, y, iterations=6):
    num = complex(x, y)
    z = complex(0, 0)
    for i in range(0, iterations):
        z = z ** 2 + num
    if mag_complex(z) > 2:
        return False
    return True


def derivative(equation, x):
    from ..string_formatting import syntax_correction
    def f(x):
        t = x
        r = x
        return eval(syntax_correction(equation))

    h = 0.0000000001
    return (f(x + h) - f(x)) / h


def newton_rhapson(equation, x0, iterations=20):
    from ..string_formatting import syntax_correction
    x = x0
    t = x0
    r = x0
    equation = syntax_correction(equation)
    for i in range(iterations):
        try:
            x = x - (eval(equation) / derivative(equation, x))
            t = x
            r = x
            return x
        except:
            break


def choose(n, r):
    return fact(n) / (fact(r) * fact(n - r))


def C(n, r):
    return choose(n, r)


# Algorithm to calculate line of best fit, see documentation
def regression(listOfPoints):
    x_sum = 0
    for point in listOfPoints:
        x_sum += point[0]
    x_mean = x_sum / len(listOfPoints)

    x2_sum = 0
    for point in listOfPoints:
        x2_sum += point[0] ** 2
    x2_mean = x2_sum / len(listOfPoints)

    y_sum = 0
    for point in listOfPoints:
        y_sum += point[1]
    y_mean = y_sum / len(listOfPoints)

    xy_sum = 0
    for point in listOfPoints:
        xy_sum += point[0] * point[1]

    xy_mean = xy_sum / len(listOfPoints)
    gradient = (x_mean * y_mean - xy_mean) / (x_mean ** 2 - x2_mean)
    y_intercept = y_mean - gradient * x_mean

    return gradient, y_intercept


def integral(function, start2, end2, rule='simpsons', equation=None,
             area=False, step=0.01):
    from ..string_formatting import syntax_correction
    if equation is not None:
        a = equation.a
        a = equation.b
        a = equation.c
        a = equation.d

    start = start2
    end = end2
    function = syntax_correction(function)

    if rule == 'trapezium':
        x = start
        t = start
        area = 0

        while x < end:
            try:
                y = eval(function)
                if area:
                    y = abs(y)
                if x == start or x + step > end:
                    area += y
                else:
                    area = area + 2 * y
                x += step
                t += step
            except:
                x += step
                t += step

        return 0.5 * step * area

    elif rule == 'simpsons':
        x = start
        t = start
        i = 0
        area = 0
        while x < end:
            try:
                y = eval(function)
                if area:
                    y = abs(y)
                if x == start or x + step > end:
                    area += y
                elif i % 2 == 0:
                    area = area + 2 * y
                elif i % 2 == 1:
                    area = area + 4 * y
                x += step
                t += step
                i += 1
            except:
                x += step
                t += step
                i += 1

        return step * area / 3
