import os
from time import sleep
import re
import sys
import json
import shlex

from manager import Manager as Mgr
from interpreter import Interpreter as Int
import errors as err
import colors as clr

start_menu_help_text = \
"""
----------------------------------------------------
quit/exit                   quits the program
help                        shows this help

ch                          if use_standard_db_path is true you can select a db from that directory
                            (only works if "use_standard_db_path" is activated)
ch [db_path]                changes the DB file to your provided file path
create [db_file] [db_name]  creates a new DB at the provided path with the provided DB_NAME
----------------------------------------------------
"""

help_text = \
"""
----------------------------------------------------
quit/exit       quits the program
help            shows this help

lsg             lists all groups in database
lsea            lists all entries in all groups
lse group_name  lists all entries in the specified group
----------------------------------------------------
"""

# checks the OS
if sys.platform == 'win32':
    os.system('cls')
    os.system('color F')
elif sys.platform == 'linux':
    import readline
    os.system('clear')

# basic settings
standard_db_path = ''
use_standard_db_path = False

# class object vars
int_ = None
mgr = None

# load config.json
try:
    with open('config.json', 'r') as cfg_r:
        json_cfg = cfg_r.read()
    cfg = json.loads(json_cfg)

    if 'standard_db_path' in cfg and not cfg['standard_db_path'].isspace() and cfg['standard_db_path'] != '':
        # checks if standard_db_path exists and is a path
        if not os.path.exists(cfg['standard_db_path']):
            print(clr.Fore.LIGHT_RED + 'The provided path wasn\'t found!\nChange your "config.json" file' + clr.RESET)
            exit(0)
        if os.path.isfile(cfg['standard_db_path']):
            print(clr.Fore.LIGHT_RED + 'The provided path can\'t be a file!\nChange your "config.json" file' + clr.RESET)
            exit(0)

        standard_db_path = cfg['standard_db_path']

        if 'use_standard_db_path' in cfg:
            use_standard_db_path = cfg['use_standard_db_path']
        else:
            use_standard_db_path = True

        if not standard_db_path.endswith('/'):
            standard_db_path += '/'             # adds a / if there is no at the end ot the standard_db_path
except FileNotFoundError:
    print(clr.Fore.YELLOW + '[i] You don\'t have a "config.json" file, using standard settings' + clr.RESET)
    pass

def quit():
    """quits the application"""
    print('\nQuitting...')
    if sys.platform == 'win32':
        os.system('cls')
        os.system('color F')
        exit(0)
    elif sys.platform == 'linux':
        os.system('clear')
        exit(0)
    sleep(1.5)

def start_menu():
    """start menu provides list of databases if 'use_standard_db_path = True' and allows to create and change a db"""
    global int_
    global mgr
    global use_standard_db_path

    while True:
        cmd = input(f'>> ')
        try:
            _cmd = shlex.split(cmd)
            if '' in _cmd:
                _cmd.remove('')
        except ValueError:
            print(clr.Fore.LIGHT_RED + 'You need to add closing quotes!' + clr.RESET)
            continue
            
        if _cmd[0] == 'help':
            print(start_menu_help_text)
        elif _cmd[0] == 'quit' or _cmd[0] == 'exit':
            quit()
        elif len(_cmd) == 1 and _cmd[0] == 'ch' and use_standard_db_path:           # if standard_db_path is set in config.json and use_standard_db_path = True,
            files_in_std_dir = os.listdir(standard_db_path)                         # this will let the user choose a .pydb file from that directory

            # searches db files and prints a list of them to choose from
            databases_counter = 0
            databases = []
            for i in files_in_std_dir:  # i is the file in files_in_std_dir
                if os.path.isfile(standard_db_path + i):
                    if i.endswith('.pydb'):
                        databases_counter += 1
                        databases.append([databases_counter, standard_db_path + i])
                        print(clr.Fore.PURPLE + f'[{databases_counter}] ' + clr.RESET + i)

            if databases_counter == 0:
                print(clr.Fore.YELLOW + '[i] There is no ".pydb" file in the given directory' + clr.RESET)
                print('')
                # use_standard_db_path = False
                continue

            print(f'\n{clr.Fore.LIGHT_RED}[q]{clr.RESET} quit\n')

            while True:
                # lets the user choose from the list
                try:
                    select_i = input('Type in the number of the database you want to use\n> ')
                    if select_i == 'q' or select_i == 'quit':
                        start_menu()
                    else:
                        db_num = int(select_i)
                except ValueError:
                    print(clr.Fore.LIGHT_RED + 'The input needs to be a non decimal number!' + clr.RESET)
                    start_menu()

                if db_num < 1 or db_num > databases_counter:
                    print(clr.Fore.LIGHT_RED + 'The number you typed in is out of range!' + clr.RESET)
                    start_menu()

                for db in databases:
                    if db_num == db[0]:
                        int_ = Int(db[1])

                        try:
                            int_.check_db_file()
                            print('Loading the database...')
                            int_.get_script()
                            int_.get_groups()
                            print('Loaded\n')

                            mgr = Mgr(db[1])
                            break
                        except err.FileNotDB as e:
                            print(e)
                        except err.DatabaseNotFound as e:
                            print(e)

                break
            break
        elif len(_cmd) == 2 and _cmd[0] == 'ch' and _cmd[1] != '' and not _cmd[1].isspace():
            int_ = Int(_cmd[1])

            try:
                int_.check_db_file()
                print('Loading the database...')
                int_.get_script()
                int_.get_groups()
                print('Loaded\n')

                mgr = Mgr(_cmd[1])
                break
            except err.FileNotDB as e:
                print(e)
            except err.DatabaseNotFound as e:
                print(e)
        elif _cmd[0] == 'ch':
            if len(_cmd) > 2:
                print(clr.Fore.LIGHT_RED + 'That are too many arguments!' + clr.RESET)

            if len(_cmd) == 2 and _cmd[1] == '' or _cmd[1].isspace():
                print(clr.Fore.LIGHT_RED + 'You have to provide a database file!' + clr.RESET)
        elif _cmd[0] == 'create':
            if len(_cmd) < 3 or _cmd[1] == '' or _cmd[2] == ''  or _cmd[1].isspace() or _cmd[2].isspace():
                print(clr.Fore.LIGHT_RED + 'You have to provide a file name or path and a DB_NAME!' + clr.RESET)
                continue
            
            db_file = _cmd[1]

            if '/' not in _cmd[1] and use_standard_db_path:
                db_file = standard_db_path + _cmd[1]

            try:
                mgr_ = Mgr(db_file)
                mgr_.create_db(_cmd[2])
            except err.DatabaseAlreadyExists as e:
                print(clr.Fore.LIGHT_RED + str(e) + clr.RESET)
                continue

            int_ = Int(db_file)
            int_.check_db_file()
            print('Loading the database...')
            int_.get_script()
            int_.get_groups()
            print('Loaded\n')

            mgr = Mgr(_cmd[1])
            break
        else:
            print(f'{clr.Fore.LIGHT_RED}"{_cmd[0]}" is an unknown command, type "help" to see a list of all available commands{clr.RESET}')

# welcome text
print('-------------------------------------------')
print('Welcome to PYDB')
print('dev v1.0')
print('type "help" for a list of available commands')
print('-------------------------------------------\n')

try:
    start_menu()

    while True:
        cmd = input(f'({clr.Fore.RED}{int_.db_name}{clr.RESET})>> ')
        # _cmd = re.split(r'\s+(?=[^"]*(?:\(|$))', cmd)
        _cmd = shlex.split(cmd)
        if '' in _cmd:
            _cmd.remove('')
        cmd = cmd.split()

        if _cmd[0] == 'exit' or cmd[0] == 'quit':
            """quits console"""
            print('\nQuitting...')
            exit(0)
        elif _cmd[0] == 'help':
            """prints help text"""
            print(help_text)
        elif _cmd[0] == 'back':
            print('\n-----Start Menu-----\ntype "help" for a list of available commands\n' + '-' * 20 + '\n')
            start_menu()
        elif _cmd[0] == 'clear':
            if sys.platform == 'win32':
                os.system('cls')
            elif sys.platform == 'linux':
                os.system('clear')
        elif _cmd[0] == 'lsg':
            """lists all groups in DB"""
            print('\n' + f'----- Groups in "{clr.Fore.PURPLE}{int_.db_name}{clr.RESET}" -----')

            if not int_.db_groups:
                print('There are no groups in this database')
                continue

            for group in int_.db_groups:
                print(clr.Fore.ORANGE + group + clr.RESET)

            print('-' * len(f'----- Groups in "{int_.db_name}" -----') + '\n')
        elif _cmd[0] == 'lsea':
            """lists all entries in all groups in DB"""
            int_.get_entries()

            print('')
            print(f'{clr.Fore.CYAN}ID\t{clr.Fore.ORANGE}Group\t\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
            for entry in int_.db_entries:
                print(clr.Fore.CYAN + entry['id'] + '\t' + clr.Fore.ORANGE + entry['group'] + '\t\t' + clr.Fore.LIGHT_GREEN + entry['name'] + clr.RESET)
            print('')
        elif _cmd[0] == 'lse':
            """lists all entries in specified group"""
            if len(cmd) < 2:
                print(clr.Fore.LIGHT_RED + 'You need to specify a group!' + clr.RESET)

            try:
                try:
                    entries_in_group = int_.get_entries_in_group(_cmd[1])
                except IndexError:
                    entries_in_group = int_.get_entries_in_group(cmd[1])

                print(f'{clr.Fore.CYAN}ID\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
                for entry in entries_in_group:
                    print(clr.Fore.CYAN + entry['id'] + '\t' + entry['name'] + clr.RESET)
            except err.GroupNotFound as e:
                print(clr.Fore.LIGHT_RED + str(e) + clr.RESET)
        else:
            print(f'{clr.Fore.LIGHT_RED}"{cmd[0]}" is an unknown command, type "help" to see a list of all available commands{clr.RESET}')

except KeyboardInterrupt:
    quit()
