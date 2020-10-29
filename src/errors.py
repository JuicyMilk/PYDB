class Error(Exception):
    """Base class for other exceptions"""
    pass


class DatabaseNotFound(Error):
    """Raised if database or path isn't found"""
    def __init__(self):
        super().__init__(f'The provided database or path wasn\'t found!')


class FileNotDB(Error):
    """Raised if file isn't a '.mypwddb'-file"""
    def __init__(self):
        super().__init__(f'The provided file or path isn\'t a ".pydb"-file!')


class NoSecurityKey(Error):
    """Raised if there is no Secure Key in the first line of the database"""
    def __init__(self):
        super().__init__('There is no Security Key(SK) in the first line of the database file!')


class WrongPassword(Error):
    """Raised if password is wrong"""
    def __init__(self):
        super().__init__('The provided password is wrong!')


class InterpretError(Error):
    def __init__(self):
        super().__init__('InterpreterError')


class GroupNotFound(Error):
    """Raised if Group isn't found"""
    def __init__(self):
        super(GroupNotFound, self).__init__("The specified group could not be found!")


class EntryNotFound(Error):
    def __init__(self):
        super(EntryNotFound, self).__init__("The specified entry could not be found!")


class DatabaseAlreadyExists(Error):
    def __init__(self):
        super(DatabaseAlreadyExists, self).__init__("The database you want to create already exists!")


class GroupAlreadyExists(Error):
    def __init__(self):
        super(GroupAlreadyExists, self).__init__("The group you want to create already exists!")


class EntryAlreadyExists(Error):
    def __init__(self):
        super(EntryAlreadyExists, self).__init__("The entry you want to create does already exist!")

class DoubleID(Error):
    def __init__(self):
        super(DoubleID, self).__init__('There are tow entries with the same ID!')
