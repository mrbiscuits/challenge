from utils import col

def fifth_interpreter(stack=[], cmd=[''], caller="cli"):
    errors = []
    while cmd[0] not in ['EXIT', 'Q', 'QUIT']:
        print(f"{col.ENDC}{col.GREY}stack is [{col.GREEN}{', '.join([str(s) for s in stack])}{col.GREY}]{col.GREEN}")
        cmd = input() if caller=='cli' else cmd
        cmd = cmd.strip().upper().split(' ')
        if cmd[0] == 'PUSH' or cmd[0] == 'P' or (len(cmd) == 1 and cmd[0].strip('-').isdigit()):
            if len(cmd) == 2 and cmd[1].strip('-').isdigit():
                stack.append(int(cmd[1]))
            else:
                if len(cmd) == 1 and cmd[0].strip('-').isdigit():
                    stack.append(int(cmd[0]))
                else:
                    errors.append(f"SYNTAX ERROR: Input should be in the form `PUSH x` where x is a valid integer, not `{' '.join(cmd)}`")
                    print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        elif cmd[0] == 'POP':
            if len(stack):
                stack.pop()
            else:
                errors.append(f"OPERATOR ERROR: Nothing to POP")
                print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        elif cmd[0] == 'SWAP':
            if len(stack) > 1:
                first = stack.pop()
                last = stack.pop()
                stack.extend([first, last])
            else:
                errors.append(f"OPERATOR ERROR: Need at least two items in the stack to perform SWAP")
                print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        elif cmd[0] == 'DUP':
            if len(stack):
                stack.append(stack[-1])
            else:
                errors.append(f"OPERATOR ERROR: Need at least one item in the stack to perform DUP")
                print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        elif cmd[0] in ['+', "-", "*", "/"]:
            if len(stack) > 1:
                first = stack.pop()
                last = stack.pop()
                if cmd[0] == '+':
                    stack.append(first + last)
                if cmd[0] == '-':
                    stack.append(first - last)
                if cmd[0] == '*':
                    stack.append(first * last)
                if cmd[0] == '/':
                    stack.append(last // first)
            else:
                errors.append(f"OPERATOR ERROR: Need at least two items in the stack to perform arithmetic")
                print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        elif cmd[0] in ['EXIT', 'Q', 'QUIT']:
            print(f"{'-'*32}\nSo long & thanks for the Fifth!")
        else:
            errors.append(f"INPUT ERROR: Input should be any of: {col.OKBLUE}PUSH x, POP, SWAP, DUP, +, -, *, /{col.ENDC}")
            print(f"{col.ORANGE}{errors[0]}{col.ENDC}")
        if caller=='api':
            return {'stack': stack, 'cmd': cmd, 'error': '<br/>'.join(errors) if len(errors) else 0}