from app.challenge.roman import fromRoman, digitise_numerals
from app.challenge.collatz import collatz_input, collatz
from app.challenge.fifth import fifth_interpreter
from utils import col
import sys, os

def main():
    print(f"{col.ENDC}{col.GREY}\n{'-'*5}{col.GREY} Available Programs{col.GREY} {'-'*30}{col.ENDC}")
    while(True):        
        print(f"\n {col.ENDC}{col.GREEN}1. Calculate # of steps for Collatz sequence to equal 1")
        print(f" {col.GREEN}2. Convert roman numerals to integers")
        print(f" {col.GREEN}3. Launch the Fifth Interpreter")
        print(f" {col.GREEN}Q. Quit\n")
        cmd = input(f'{col.GREY}Please select a program: {col.BOLD}{col.GREEN}').upper()
        print(f"{col.ENDC}{col.GREEN}")
        if cmd == "1":
            # print(f"Program selected: COLLATZ\n{'-'*40}")
            collatz_input()
        if cmd == "2":
            # print(f"Program selected: NUMERALS\n{'-'*40}")
            digitise_numerals()
        if cmd == "3":
            # print(f"Program selected: FIFTH INTERPRETER\n{'-'*40}")
            fifth_interpreter()
        if cmd in ['EXIT', 'Q', 'QUIT']:
            print(f"{col.ENDC}{col.GREEN}Bye!\n")
            break

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    try:
        main()
    except KeyboardInterrupt:
        print(f"{col.ENDC}\n\n{col.GREEN}Bye!\n")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
