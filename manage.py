import sys
import subprocess
import os
from settings import *
from utils import col 
import random 
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
goodbye_msgs = ["See you!", "Goodbye"]
welcome_msgs = ["Hello","Welcome "]

try:
    import click
except:
    print("You must create a py3 virtualenv and install the requirements to use this file.")
    install = input("Would you like to automate install at PROJECT_ROOT/venv? Y/N: ")
    if install.upper().strip() == 'Y':
        print(f"Installing venv at {PROJECT_ROOT}/{VENV_NAME}...")
        os.system(f'python3 -m venv {VENV_NAME}')
        print(f'Activating env at {PROJECT_ROOT}/{VENV_NAME}/bin/activate')
        os.system(f"source {VENV_NAME}/bin/activate && pip install -r requirements.txt")
        os.system(f"source {VENV_NAME}/bin/activate && python manage.py menu")
        activate_script = os.path.join(PROJECT_ROOT, 'scripts', 'activate_this.py')
        with open(activate_script) as f:
            code = compile(f.read(), activate_script, 'exec')
            exec(code, dict(__file__=activate_script))

    if install.upper().strip() == 'N':
        print(f"Attempting to use {col.ORANGE}{VENV_NAME}/bin/activate{col.ENDC}, did you forget to activate it?")
        os.system(f"source {VENV_NAME}/bin/activate && python manage.py menu")
    print(f"\n{col.GREY}\n{'-'*40}\n{col.GREEN}Please activate your venv before running again: \n{col.OKBLUE}source {VENV_NAME}/bin/activate && python manage.py menu\n{col.ENDC}")
    sys.exit()

@click.group()
@click.version_option(0.1, '-V', '--version', prog_name='challenge-app')
def cli():
    pass

@cli.command()
@click.argument('command')
def init(command, **config):
    """
    Welcome to the launcher for the Challenge app.  
    To use the launcher, please invoke this script like so:

    python manage.py menu - view interactive menu\n
    python manage.py COMMAND - execute a command (one of: cli, runserver, shell, test, coverage, quit)
    """
    choice = command
    if command == 'menu':
        print(get_menu())
        choice = input()
        print("\033[A                             \033[A\n")    # ansi escape arrow up then overwrite the line

    if choice in ['1', 'cli']:
        os.system(f"python ./")

    if choice in ['2', 'run', 'go', 'up', 'runserver']:
        if command == 'menu':
            os.system(f"source {VENV_NAME}/bin/activate && python manage.py run")
        else:
            from app.bootstrap import bootstrap, configure_postfork_logging
            from flask import json
            app = bootstrap()
            app.debug = True
            app.run(host="0.0.0.0", port=5050, threaded=False, debug=True)

    elif choice in ['3', 'shell']:
        try:
            import IPython
            IPython.start_ipython(argv=[])
        except:
            from code import InteractiveConsole
            InteractiveConsole(locals=globals()).interact()

    elif choice in ['4', 'test']:
        os.system(f'source {VENV_NAME}/bin/activate && pytest --cov="{PROJECT_ROOT}" -v -s')
        # os.system(f'mv htmlcov app/templates')

    elif choice in ['5', 'coverage', 'cov']:
        os.system(f'source {VENV_NAME}/bin/activate && pytest --cov="{PROJECT_ROOT}" --cov-report html -p no:sugar -vvvv')
        # os.system(f'mv htmlcov app/templates')

    if choice in ['q', 'quit', 'bye', '10', 'QUIT', 'BYE']:
        print(f"""    {col.GREY}{col.EM}{random.choice(goodbye_msgs)}{col.ENDC}\n""")

def get_menu():
    return f"""
{col.DARKBLUE}｀、ヽ {col.BOLD}T&T {col.EM}{col.GREEN}CANDIDATES{col.ENDC}{col.DARKBLUE} ヽ｀ ヽヽ｀ヽ｀、ヽヽ｀ヽ｀、｀ヽ｀、ヽヽ｀ヽ｀、ヽヽヽ｀、ヽヽ ヽ｀ヽ｀、{col.ENDC}

 {col.EM}{col.OKBLUE}Make sure settings.py is configured{col.ENDC}                        {col.EM}{col.GREY}Ctrl-C to quit{col.ENDC}
{col.GREY}---------------------------------------------------------------------------------{col.ENDC}
 {col.GREY}{col.EM}{random.choice(welcome_msgs)}{col.ENDC}
 
 {col.EM}{col.PURPLE}1.{col.ENDC} Launch challenge CLI program
 {col.EM}{col.PURPLE}2.{col.ENDC} Run Flask devserver
 {col.EM}{col.PURPLE}3.{col.ENDC} Start a Shell Session
 {col.EM}{col.PURPLE}4.{col.ENDC} Run Tests
 {col.EM}{col.PURPLE}5.{col.ENDC} Run Tests and generate a HTML coverage report
 
 {col.EM}{col.PURPLE}Q.{col.ENDC} Quit"""

from click._compat import get_text_stderr
from click.utils import echo
def show(self, file=None):
    if file is None:
        file = get_text_stderr()
    color = None
    hint = ''
    if (self.cmd is not None and
            self.cmd.get_help_option(self.ctx) is not None):
        hint = (f'''
{col.OKGREEN}-----------------------------------------------------------------------{col.ENDC}
To use the launcher, please invoke the script like so:
{col.OKGREEN}-----------------------------------------------------------------------{col.ENDC}
"python manage.py.py menu" to view options
"python manage.py.py COMMAND" to execute a command
"python manage.py.py --help" for help.
''')
    if self.ctx is not None:
        color = self.ctx.color
        echo(self.ctx.get_usage() + '\n%s' % hint, file=file, color=color)
    echo('Error: %s' % self.format_message(), file=file, color=color)

click.exceptions.UsageError.show = show

if __name__ == "__main__":
   init()
