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

            # FIXME: TODO: make re.search safe, so value won't be scanned
            if re.search(r'ENTRY\[id="(\d)", name="(.?)", group="' + group + r'"', line):
                entry_indx = script.index(line)

                script.remove(line)
                script.insert(entry_indx, line.replace(f'group="{group}"', f'group="{new_group_name}"'))
            
        with open(self.db, 'w') as group_edit:
            for line in script:
                group_edit.write(line + '\n')

    def add_entry(self, name: str, group: str, data_type='', value='', id_value=''):
        """adds entry to database"""
        self.int_.get_groups()

        entries_in_group = self.int_.get_entries_in_group(group)
        
        # check id first
        entry_ids = []
        for entry in entries_in_group:
            if id_value == entry['id']:
                raise err.DoubleID
            entry_ids.append(entry['id'])
        
        if id_value == 'AUTO':
            if entry_ids == []:
                id_value = 1
            else:
                id_value = int(max(entry_ids)) + 1

        # checks data types
        data_types = ['int', 'float', 'string', 'bool', 'date', 'text']

        if value == '':
            pass
        else:
            try:
                if data_type == data_types[0]:      # int
                    value = int(value)
                elif data_type == data_types[1]:    # float
                    value = float(value)
                elif data_type == data_types[2]:    # string
                    value = str(value)
                elif data_type == data_types[3]:    # bool
                    if value.lower() != 'true' and value.lower() != 'false' and value != '0' and value != '1':
                        raise err.DBValueError
                    value = bool(value.lower())
                elif data_type == data_types[4]:    # date
                    if not re.search('^(\d)(\d)/(\d)(\d)/(\d)(\d)(\d)(\d)$', str(value)):
                        raise err.DBValueError
                elif data_type == data_types[5]:    # text
                    if not value.isalpha():
                        raise err.DBValueError
            except ValueError:
                raise err.DBValueError

        entry = f'ENTRY[id="{id_value}", name="{name}", group="{group}", type="{data_type}", value="{value}"]'

        # check where to add the entry
        # TODO: remove unnecessary blank lines in db file
        script = self.int_.script_lines

        if re.search(r'^ENTRY\[id="(\d+)", name="(.+?)", group="(.+?)", type="(.*?)", value="(.*?)"]$', script[len(script) - 1]):

            script.append(entry)

            with open(self.int_.db, 'w') as add_entry_f:
                for line in script:
                    add_entry_f.write(line + '\n')

        else:
            script.append('')
            script.append(entry)

            with open(self.int_.db, 'w') as add_entry_f:
                for line in script:
                    add_entry_f.write(line + '\n')

    def remove_entry(self, entry: str):
        pass

    def edit_entry(self, entry: str):
        pass
