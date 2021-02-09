# PYDB (dev version)
*Simple Database System in Python*

PYDB (dev version) is a simple database system written fully in python.
Its structure is very easy to understand and to read.

For example:

**example.pydb**
```
DB_NAME["example"]

GROUP[name="Group_1"]
GROUP[name="Group_2"]

ENTRY[id="1", name="EntryOne", group="Group_2", type="int", value="10"]
ENTRY[id="2", name="EntryTwo", group="Group_2", type="string", value="Hello World!"]
ENTRY[id="1", name="EntryOne", group="Group_1", type="float", value="10.57"]
```

`DB_NAME`: There is the name of the database stored, it can be different from the file name but it's good practice to keep them the same

`GROUP`: Groups are there for the basic structure. Groups are similar to classes in Python

`ENTRY`: Entries are the actual data store. They always belong to a group. Entries are similar to class functions in Python.

## Usage
To be able to use PYDB in your own projects you have to import some modules.
These modules are stored in `src/`. But you could also use the `console.py` file to work with the databases directly.
Here you can see what imports you need.

```python
import interpreter.Interpreter
import manager.Manager
import errors
```

`interpreter.Interpreter`: This is the interpreter class. Its used to get all the groups and entries in your database.

`manager.Manager`: This is used to edit your database and its components.

`errors`: And of course you should be able to handle errors. A list of all errors can be found below.

I'll now show you a basic example of how to use PYDB.
Let's say you don't like the console I made and you want to design your own.
The next script lets you choose a database and show the groups in it.

**your_console.py**
```python
from interpreter import Interpreter as Int
from manager import Manager as Mgr
import errors as err

# pre-defining your Interpreter object
int_ = None

# Let's you select a database file
db_file = input('Enter the path to your PYDB database\n>> ')

try:
    int_ = Int(db_file)
    int_.check_db_file()
except err.FileNotDB as e:
    print(e)
    exit(0)
except err.DatabaseNotFound as e:
    print(e)
    exit(0)

command = input(int_.db_name + '> ')
if command == 'lsg':    # lists all groups
    int_.get_groups()

    print('-----GROUPS-----')
    for group in int_.db_groups:
        print(group)
    print('----------------')
```

## Errors
*coming*
