from utils import col

def collatz_input(number = False, caller="cli"):
    steps = 0
    while type(number) is not int:
        if not number:
            number = input(f"{col.ENDC}{col.GREY}Enter a number: {col.GREEN}")
        number = int(number) if number.isdigit() else 0
        if number <= 1:
            print(" Please enter a number greater than 1")
            number = False
            if caller == "api":
                return {'error':  "Please enter a number greater than 1"}

    while number > 1:
        steps += 1
        number = collatz(number)
    print(f"{col.ENDC}{col.GREY}Number of steps: {col.BOLD}{col.OKBLUE}{steps}")
    return {'number': number, 'steps': steps}

def collatz(number):
    if number % 2 == 0:
        return number / 2
    else:
        return 3 * number + 1