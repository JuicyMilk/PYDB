import os

from interpreter import Interpreter as Int
import errors as err
import colors as clr

class Manager:
    def __init__(self, db_path: str):
        self.db = db_path
        self.int_ = Int(self.db)

    def create_db(self, db_name: str):
        if not self.db.endswith('.pydb'):
            raise err.FileNotDB

        if db_name == '' or db_name.isspace():
            raise err.DBNameEmpty

        if os.path.exists(self.db):
            raise err.DatabaseAlreadyExists

        with open(self.db, 'w+') as db_creator:
            db_creator.write(f'DB_NAME["{db_name}"]')
            db_creator.flush()
            db_creator.seek(0)
            db_creator.close()

    def remove_db(self):
        pass

    def add_group(self, group_name: str):
        self.int_.get_groups()

        if group_name in self.int_.db_groups:
            raise err.GroupAlreadyExists

        group_schema = f'\nGROUP[name="{group_name}"]'
        with open(self.db, 'a') as group_writer:
            group_writer.write(group_schema)

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
