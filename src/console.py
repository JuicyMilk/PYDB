import os
from time import sleep
import re
import sys
import json

from interpreter import Interpreter as Int
import errors as err
import colors as clr

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

if sys.platform == 'win32':
    # os.system('cls')
    os.system('color F')
elif sys.platform == 'linux':
    import readline
    # os.system('clear')

# basic settings
standard_db_path = ''
use_standard_db_path = False

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
            standard_db_path + '/'
except FileNotFoundError:
    print(clr.Fore.YELLOW + '[i] You don\'t have a "config.json" file, using standard settings' + clr.RESET)
    pass

print('-------------------------------------------')
print('Welcome to PYDB')
print('alpha v1.0')
print('type "help" for a list of available commands')
print('-------------------------------------------\n')

try:
    # if standard_db_file is set in config.json and use_standard_db_file = True,
    # this will let the user choose a .pydb file from that directory
    while True:
        if use_standard_db_path:
            files_in_std_dir = os.listdir(standard_db_path)

            # searches db files and prints a list of them to choose from
            databases_counter = 0
            databases = []
            for i in files_in_std_dir:
                if os.path.isfile(standard_db_path + i):
                    if i.endswith('.pydb'):
                        databases_counter += 1
                        databases.append([databases_counter, standard_db_path + i])
                        print(clr.Fore.PURPLE + f'[{databases_counter}] ' + clr.RESET + i.replace('.pydb', ''))

            if databases_counter == 0:
                print(clr.Fore.YELLOW + '[i] There is no ".pydb" file in the given directory' + clr.RESET)
                print('Quitting')       # TODO let user create DB if there is no DB
                exit(0)

            while True:
                # lets the user choose from the list
                try:
                    db_num = int(input('Type in the number of the database you want to use\n> '))
                except ValueError:
                    print(clr.Fore.LIGHT_RED + 'The input needs to be a non decimal number!' + clr.RESET)
                    continue

                if db_num < 1 or db_num > databases_counter:
                    print(clr.Fore.LIGHT_RED + 'The number you typed in is out of range!' + clr.RESET)
                    continue

                for db in databases:
                    if db_num == db[0]:
                        int_ = Int(db[1])

                        try:
                            int_.check_db_file()
                            break
                        except err.FileNotDB as e:
                            print(e)
                        except err.DatabaseNotFound as e:
                            print(e)
                break
            break   # if chosen right, database gets loaded
        else:
            db_path = input('Enter the DB file path: ')
            int_ = Int(db_path)

            try:
                int_.check_db_file()
                break
            except err.FileNotDB as e:
                print(e)
            except err.DatabaseNotFound as e:
                print(e)

    print('Loading the database...')
    int_.get_script()
    int_.get_groups()
    print('Loaded\n')

    while True:
        cmd = input(f'({clr.Fore.RED}{int_.db_name}{clr.RESET})>> ')
        _cmd = re.split(r'\s+(?=[^"]*(?:\(|$))', cmd)
        cmd = cmd.split()

        if cmd[0] == 'exit' or cmd[0] == 'quit':
            """quits console"""
            print('\nQuitting...')
            exit(0)
        elif cmd[0] == 'help':
            """prints help text"""
            print(help_text)
        elif cmd[0] == 'lsg':
            """lists all groups in DB"""
            print('\n' + f'----- Groups in "{clr.Fore.PURPLE}{int_.db_name}{clr.RESET}" -----')

            if not int_.db_groups:
                print('There are no groups in this database')
                continue

            for group in int_.db_groups:
                print(clr.Fore.ORANGE + group + clr.RESET)

            print('-' * len(f'----- Groups in "{int_.db_name}" -----') + '\n')
        elif cmd[0] == 'lsea':
            """lists all entries in all groups in DB"""
            int_.get_entries()

            print('')
            print(f'{clr.Fore.CYAN}ID\t{clr.Fore.ORANGE}Group\t\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
            for entry in int_.db_entries:
                print(clr.Fore.CYAN + entry['id'] + '\t' + clr.Fore.ORANGE + entry['group'] + '\t\t' + clr.Fore.LIGHT_GREEN + entry['name'] + clr.RESET)
            print('')
        elif cmd[0] == 'lse':
            """lists all entries in specified group"""
            if not len(cmd) >= 2 or cmd[1] == '':
                print(clr.Fore.LIGHT_RED + 'You need to specify a group!' + clr.RESET)
                continue

            int_.get_groups()
            int_.get_entries()
            print('')

            # checks if " ar in _cmd
            if '"' in _cmd[0]:
                group_name = re.findall(r'"(.*?)"', _cmd[0])[0]

                # if yes, print entry
                if group_name in int_.db_groups:
                    print(f'{clr.Fore.CYAN}ID\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
                    for entry in int_.db_entries:
                        if entry['group'] == group_name:
                            print(clr.Fore.CYAN + entry['id'] + '\t' + clr.Fore.LIGHT_GREEN + entry['name'] + clr.RESET)
                            print('')
                            break
                    continue
                else:
                    print
                    print(clr.Fore.LIGHT_RED + f'The group "{group_name}" does not exist!"' + clr.RESET)
                    continue

            # prints entries that don't have spaces in name
            if cmd[1] not in int_.db_groups:
                print(clr.Fore.LIGHT_RED + f'The group "{cmd[1]}" does not exist!"' + clr.RESET)
                continue
            int_.get_entries()

            print(f'{clr.Fore.CYAN}ID\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
            for entry in int_.db_entries:
                if entry['group'] == cmd[1]:
                    print(clr.Fore.CYAN + entry['id'] + '\t' + clr.Fore.LIGHT_GREEN + entry['name'] + clr.RESET)
            print('')
        else:
            print(f'{clr.Fore.RED}"{cmd[0]}" is an unknown command, type help to see a list of all available commands{clr.RESET}')

except KeyboardInterrupt:
    print('\nQuitting...')
    if sys.platform == 'win32':
        # os.system('cls') TODO add this again later
        os.system('color F')
    elif sys.platform == 'linux':
        # os.system('clear') TODO add this again later
        pass
    # sleep(1.5) TODO add this again later
