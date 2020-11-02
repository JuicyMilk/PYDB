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
        """adds group to database"""
        self.int_.get_groups()
        script = self.int_.script_lines

        if group_name in self.int_.db_groups:
            raise err.GroupAlreadyExists

        for line in script:
             if line.isspace() or line == '':
                 script.remove(line)

        group_schema = f'GROUP[name="{group_name}"]'
        
        script_indx_db_name = next(line for line in script if line == f'DB_NAME["{self.int_.db_name}"]')
        script_ = []

        script_.append(script[script.index(script_indx_db_name)] + '\r\n')
        if any('GROUP[name="' in line for line in script):
            for line in script:
                if line == f'DB_NAME["{self.int_.db_name}"]':
                    continue
                if 'ENTRY[' in line:
                    script_.insert(''.join(script_).rindex('GROUP[name="'), group_schema + '\r\n')
                script_.append(line + '\n')
        else:
            script_.append(group_schema + '\n\n')
        
        script_[-1] = script_[-1].replace('\n', '')
        with open(self.db, 'w') as group_add:
            for line in script_:
                group_add.write(line)

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
