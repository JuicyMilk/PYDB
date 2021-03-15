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
            if line == f'GROUP[name="{group}"]':
                script.remove(line)

        for line in script:
            if 'ENTRY[id=' in line and f'group="{group}"' in line:
                script.remove(line)

        if script[-1] == '':
            del script[-1]

        with open(self.db, 'w') as group_rm:
            for line in script:
                group_rm.write(line + '\n')

    def edit_group(self, group: str, new_group_name: str):
        """changes group name"""
        entries_in_group = self.int_.get_entries_in_group(group)
        script = self.int_.script_lines

        if new_group_name in self.int_.db_groups:
            raise err.GroupAlreadyExists

        for line in script:
            if line == f'GROUP[name="{group}"]':
                group_indx = script.index(line)
                script.remove(line)
                script.insert(group_indx, f'GROUP[name="{new_group_name}"]')

            if re.search(r'ENTRY\[id="(\d)", name="(.?)", group="' + group + r'"', line):
                entry_indx = script.index(line)

                script.remove(line)
                script.insert(entry_indx, line.replace(f'group="{group}"', f'group="{new_group_name}"'))
            
        with open(self.db, 'w') as group_edit:
            for line in script:
                group_edit.write(line + '\n')

    def add_entry(self, name: str, group: str, data_type=None, value=None, id_value=None):
        """adds entry to database"""
        # TODO: add entry to db
        self.int_.get_groups()

        entries_in_group = self.int_.get_entries_in_group(group)
        print(entries_in_group)

    def remove_entry(self, entry: str):
        pass

    def edit_entry(self, entry: str):
        pass
