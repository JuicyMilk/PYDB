import os
from time import sleep
import re
import sys

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

print('-------------------------------------------')
print('Welcome to PYDB')
print('alpha v1.0')
print('type "help" for a list of available commands')
print('-------------------------------------------\n')

try:
    while True:
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
            print('\nQuitting...')
            exit(0)
        elif cmd[0] == 'help':
            print(help_text)
        elif cmd[0] == 'lsg':
            print('\n' + f'----- Groups in "{int_.db_name}" -----')

            if not int_.db_groups:
                print('There are no groups in this database')
                continue

            for group in int_.db_groups:
                print(group)

            print('-' * len(f'----- Groups in "{int_.db_name}" -----') + '\n')
        elif cmd[0] == 'lsea':
            int_.get_entries()

            print('')
            print(f'{clr.Fore.CYAN}ID\t{clr.Fore.ORANGE}Group\t\t{clr.Fore.LIGHT_GREEN}Name\n{clr.RESET}')
            for entry in int_.db_entries:
                print(clr.Fore.CYAN + entry['id'] + '\t' + clr.Fore.ORANGE + entry['group'] + '\t\t' + clr.Fore.LIGHT_GREEN + entry['name'] + clr.RESET)
            print('')
        elif cmd[0] == 'lse':
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
    # sleep(1.5) TODO add this again later
