import os
import re

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

        if self.int_.db_groups == []:
            script.insert(1, '')
            script.insert(2, f'GROUP[name="{group_name}"]')
        else:
            for line in script:
                if re.search(r'GROUP\[name="(.*?)"]', line):
                    try:
                        if not re.findall(r'GROUP\[name="(.*?)"]', script[script.index(line) + 1]):
                            script.insert(script.index(line) + 1, f'GROUP[name="{group_name}"]')
                            break
                    except IndexError:
                            script.insert(script.index(line) + 1, f'GROUP[name="{group_name}"]')
                            break

        with open(self.db, 'w') as group_add:
            for line in script:
                group_add.write(line + '\n')

    def remove_group(self, group: str):
        """removes group from db with all its entries"""
        entries_in_group = self.int_.get_entries_in_group(group)
        script = self.int_.script_lines

        for line in script:
            if line.isspace() or line == '':
                script.remove(line)

        for line in script:
            if line == f'GROUP[name="{group}"]':
                script.remove(line)

        for line in script:
            if 'ENTRY[id=' in line and f'group="{group}"' in line:
                script.remove(line)

        script.insert(1, '')

        with open(self.db, 'w') as group_rm:
            for line in script:
                group_rm.write(line + '\n')

    def edit_group(self, group: str):
        pass

    def add_entry(self, entry: str):
        pass

    def remove_entry(self, entry: str):
        pass

    def edit_entry(self, entry: str):
        pass
