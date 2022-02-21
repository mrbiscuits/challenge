import re
from utils import col

# Define exceptions
class RomanError(Exception):
    pass

class EmptyInputError(RomanError):
    pass

class InvalidRomanNumeralError(RomanError):
    pass

romanNumeralMap = (('M', 1000),
                   ('CM', 900),
                   ('D', 500),
                   ('CD', 400),
                   ('C', 100),
                   ('XC', 90),
                   ('L', 50),
                   ('XL', 40),
                   ('X', 10),
                   ('IX', 9),
                   ('V', 5),
                   ('IV', 4),
                   ('I', 1))

# Define pattern to detect valid Roman numerals
romanNumeralPattern = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """, re.VERBOSE)

def fromRoman(numeral):
    """convert Roman numeral to integer"""
    if not numeral:
        raise EmptyInputError("Input cannot be blank")

    if not romanNumeralPattern.search(numeral):
        raise InvalidRomanNumeralError(f'{numeral}: Invalid Roman numeral')

    result = 0
    index = 0
    for roman, value in romanNumeralMap:
        while numeral[index:index + len(roman)] == roman:
            result += value
            index += len(roman)
    return result

def digitise_numerals(numerals = False, caller="cli"):
    if caller != "api":
        numerals = input(f"{col.GREY}Enter roman numerals to digitise, can be seperated by a comma: {col.GREEN}")
    numerals = [n.strip().upper() for n in numerals.split(',')]
    results = []
    errors = []
    for numeral in numerals:
        try:
            results.append(fromRoman(numeral))
            print(f"{col.ENDC}{col.GREY}{numeral}: {col.OKBLUE}{results[-1]}", end=' ')
        except Exception as e:
            errors.append(f'{type(e).__name__.upper()}: {str(e)}')
            if not type(e).__name__ == "EmptyInputError":
                print(f'{str(e)}')
    print(f"\n{col.GREY}Total: {col.OKBLUE}{col.BOLD}{sum(results)}")
    return {'results':results, 'error': '<br/>'.join(errors) if len(errors) else 0}

