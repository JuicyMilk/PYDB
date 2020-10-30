import os

from interpreter import Interpreter as Int
import errors as err
import colors as clr

class Manager:
    def __init__(self, db_path: str):
        self.db = db_path
        self.int_ = Int(self.db)

    def create_db(self, db_name: str):
        pass

    def remove_db(self):
        pass

    def add_group(self, group: str):
        pass

    def remove_group(self, group: str):
        pass

    def edit_group(self, group: str):
        pass

    def add_entry(self, entry: str):
        pass

    def remove_entry(self, entry: str):
        pass

    def edit_entry(self, entry: str):
        pass
