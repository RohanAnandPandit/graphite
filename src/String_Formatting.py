from maths.Mathematical_Constants import *
from maths.Mathematical_Functions import *
from utils import invert

constants = ['π', 'φ']

# Superscript numbers,variables and operator characters
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # Regular numbers

super_script = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', 'ᵃ', 'ᵇ', 'ᶜ', 'ᵈ', 'ᵉ', 'ˢ',
                'ˣ', 'ʸ', 'ᶻ', 'ᵗ', 'ᵒ', '⁽', '⁾', '⁻', '⁺', '^', 'ᵍ', 'ᵐ', 'ʰ', 'ᶦ', 'ⁿ', '˚', 'ʳ']
variables = ['a', 'b', 'c', 'd', 'e', 't', 'x', 'y', 'z', 'r']  # Regular variables

to_super_script = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶',
                   '7': '⁷', '8': '⁸', '8': '⁹', 'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ',
                   'o': 'ᵒ', 's': 'ˢ', 'e': 'ᵉ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ', 't': 'ᵗ',
                   'g': 'ᵍ', 'm': 'ᵐ', 'h': 'ʰ', 'i': 'ᶦ', 'n': 'ⁿ', 'r': 'ʳ', '(': '⁽',
                   ')': '⁾', '-': '⁻', '*': '*', '/': '/', ' ': ' ', '+': '⁺', '*': '˚',
                   "'": "'", ',': ','}

identifiers = {'cos': '[', 'sin': ']', 'tan': '@', 'sec': '~', 'cosec': '#', 'cot': '$',
               'gamma': ';', 'asin': '%', 'acos': '_', 'atan': '&', 'sqrt': '¬',
               'cbrt': "\\", 'abs': '{', 'sigma': 'Σ', 'integral': '∫', 'fact': '£',
               'mandelbrot': '?', 'derivative': 'α', 'newtonRhapson': 'β', 'C': 'δ'}

characters = ['[', ']', '@', '~', '#', '$', ';', '%', '_', '&', '¬', "\\", '{', '}', 'Σ',
              '∫', '£', '?', 'α', 'β', 'δ']


def syntax_correction(equation, replace_functions=True):
    # This section removes all superfluous spaces from the string
    equation = list(equation)
    i = 0
    l = len(equation)
    while i < l:
        char = equation[i]
        if char == ' ':
            del equation[i]
            l -= 1
        else:
            i += 1

    # This section replaces each special character with it' syntax representation
    i = 0
    l = len(equation)
    while i < l:
        char = equation[i]
        if i < l - 1:
            # This indicates that the base is being raised to the power of the
            # expression with the supersScript brackets
            if char not in super_script and equation[i + 1] == '⁽':
                equation[i + 1] = '**('

        if char in operators + constants + super_script:
            try:
                equation[i] = key[char]
            except:
                pass
        i = i + 1

    # This section inserts the factorial function in the correct position
    # whenever the '!' symbol is encountered
    i = 0
    equation = list(''.join(equation))
    l = len(equation)
    while i < l:
        if equation[i] == '!':
            equation[i] = ')'
            if i == 0:
                equation.insert(0, 'fact(')
            else:
                j = i - 1
                while equation[j] not in operators and j >= 1:
                    j -= 1
                equation.insert(j + 1, 'fact(')
            i += 2
            l += 1
        else:
            i += 1

    # This section replaces each mathematical function with it's special
    # identifier
    equation = list(''.join(equation))
    i = 0
    l = len(equation)
    while i < l:
        for a in range(3, 11):
            if i + a < l:
                if ''.join(equation[i:i + a]) in functions:
                    equation = equation[0:i]
                    equation += [identifiers[''.join(equation[i:i + a])]]
                    equation += equation[i + a: l]
                    l = l - (a - 1)
        i = i + 1

    # This section inserts a '*' sign between expression which have been
    # implicitly multiplied
    equation = list(''.join(equation))
    for i in range(1, len(equation)):
        char = equation[i]
        if char in variables and equation[i - 1] not in operators + characters:
            equation[i] = '*' + equation[i]
        elif char == '(' and equation[i - 1] == ')':
            equation[i] = '*' + equation[i]
        elif char not in variables + operators + ['i'] and equation[i - 1] in variables:
            equation[i] = '*' + equation[i]
        elif ((char not in variables + operators + constants + numbers + ['.'])
              and (equation[i - 1] not in variables + operators + constants + numbers + ['.'])
              or (char not in variables + operators and equation[i - 1] == ')')):
            equation[i] = '*' + equation[i]

    # This section replaces special constants with their variable representation
    equation = list(''.join(equation))
    for i in range(0, len(equation)):
        if equation[i] == 'π':
            if i != 0:
                if equation[i - 1] in operators:
                    equation[i] = 'pi'
                else:
                    equation[i] = '*pi'
            else:
                equation[i] = 'pi'
        elif equation[i] == 'φ':
            if i != 0:
                if equation[i - 1] in operators:
                    equation[i] = 'phi'
                else:
                    equation[i] = '*phi'
            else:
                equation[i] = 'phi'

    # This replaces the identifier characters with the original function
    if replace_functions:
        equation = list(''.join(equation))
        for i in range(len(equation)):
            char = equation[i]
            for function in functions:
                if identifiers[function] == char:
                    equation[i] = function

    # This section inserts the absolute value function whenever the modulus
    # sign is encountered
    i = 0
    equation = list(''.join(equation))
    l = len(equation)
    tracker = True
    for i in range(len(equation)):
        if equation[i] == '|':
            if tracker:
                equation[i] = 'abs('
            else:
                equation[i] = ')'
        elif equation[i] in operators:
            # A tracker has to be maintained to mdetermine whether the modulus
            # sign is closing or opening the function
            # as the open and close modulus signs both are represented by '|'
            tracker = invert(tracker)
    return ''.join(equation)


# Formats mathematical statements entered into a form
def entry_formatter(entry):
    l = len(entry.get())
    i = 0
    while i < l:
        if i != 0:
            # If the character before the current character is in super_script
            # then the current character should also be in super_script
            if entry.get()[i - 1] in super_script and entry.get()[i] not in super_script:
                s = entry.get()[i]
                entry.delete(i)
                entry.insert(i, to_super_script[s])

            # If the user wants to raise something to a power then it will be
            # replaced by super script open bracket
            if entry.get()[i] == '^' and entry.get()[i - 1] not in super_script:
                entry.delete(i, i + 1)
                entry.insert(i, '⁽')
                entry.icursor(i + 2)

        if i + 4 < len(entry.get()) + 1:  # Ensures there are at least 4 characters left
            # If the user types sqrt it will be replaces by the symbol for square root
            if entry.get()[i:i + 4] == 'sqrt':
                entry.delete(i, i + 4)
                entry.insert(i, '√()')
                entry.icursor(i + 2)
                l = l - 1  # The length of the string is reduced by one

            # If the user types cbrt it will be replaces by the symbol for cube root
            elif entry.get()[i:i + 4] == 'cbrt':
                entry.delete(i, i + 4)
                entry.insert(i, '∛()')
                entry.icursor(i + 2)
                l = l - 1  # The length of the string is reduced by one

        if i + 2 < len(entry.get()) + 1:  # Ensures there are at least 2 characters left
            # If the user types pi it will be replaced by π
            if entry.get()[i:i + 2] == 'pi':
                entry.delete(i, i + 2)
                entry.insert(i, 'π')
                l = l - 1  # The length of the string is reduced by one

        # Ensures there are at least 3 characters left
        if i + 3 < len(entry.get()) + 1:
            # If the user types 'sum' it will be replaced by the greek letter sigma
            if entry.get()[i:i + 3] == 'sum':
                entry.delete(i, i + 3)
                entry.insert(i, 'Σ()')
                entry.icursor(i + 2)
                # l = l - 0 # The length of the string is reduced by zero
            # If the user types phi it will be replaced by the greek letter phi
            if entry.get()[i:i + 3] == 'phi':
                entry.delete(i, i + 3)
                entry.insert(i, 'φ')
                l = l - 2  # The length of the string is reduced by two

        if i + 5 < len(entry.get()) + 1:  # Ensures there are at least 5 characters left
            # If the user types sigma it will be replaced by the greek letter sigma
            if entry.get()[i:i + 5] == 'sigma':
                entry.delete(i, i + 5)
                entry.insert(i, 'Σ()')
                entry.icursor(i + 2)
                l = l - 2  # The length of the string is reduced by two

        if i + 4 < len(entry.get()) + 1:  # Ensures there are at least 4 characters left
            # If the user types inte it will be replaced by the integral symbol
            if entry.get()[i:i + 4] == 'inte':
                entry.delete(i, i + 4)
                entry.insert(i, '∫()')
                entry.icursor(i + 2)
                l = l - 1  # The length of the string is reduced by one
        i += 1
    return


def substitute_values(obj, equation):
    i = 0
    equation = list(equation)
    l = len(equation)
    while (i < l):
        for a in range(3, 6):
            if (i + a < l):
                if (''.join(equation[i:i + a]) in functions):
                    equation = equation[0:i]
                    equation += [identifiers[''.join(equation[i:i + a])]]
                    equation += equation[i + a:l]
                    l = l - (a - 1)
        i = i + 1

    equation = list(equation)
    for i in range(0, len(equation)):
        char = equation[i]
        if char in ['a', 'b', 'c', 'd']:
            equation[i] = str(round(eval('obj.' + char), 3))
        elif char in numbers:
            pass
        else:
            try:
                if key[char] in ['a', 'b', 'c', 'd']:
                    equation[i] = str(round(eval('obj.' + key[char]), 3))
            except:
                pass
            try:
                if key[char] in numbers:
                    equation[i] = str(key[char])
            except:
                pass

    equation = list(''.join(equation))
    for i in range(len(equation)):
        char = equation[i]
        for function in functions:
            if identifiers[function] == char:
                equation[i] = function

    return ''.join(equation)
