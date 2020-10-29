import os
from time import sleep

from interpreter import Interpreter as Int
import errors as err
import colors as clr

# os.system('cls')
os.system('color F')

print('-------------------------------------------')
print('Welcome to PYDB')
print('alpha v1.0')
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

        if cmd == 'lsg':
            print('\n' + f'----- Groups in "{int_.db_name}" -----')

            if not int_.db_groups:
                print('There are no groups in this database')
                continue

            for group in int_.db_groups:
                print(group)

            print('-' * len(f'----- Groups in "{int_.db_name}" -----') + '\n')
        elif cmd == 'exit':
            print('\nQuitting...')
            exit(0)
except KeyboardInterrupt:
    print('\nQuitting...')
    # sleep(1.5) TODO add this again later
    # os.system('cls') TODO add this again

