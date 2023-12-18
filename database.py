import csv
import os


class CsvReader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def read_csv(self):
        result_data = []
        for files_path in self.file_paths:
            try:
                with open(files_path) as csv_file:
                    rows = csv.DictReader(csv_file)
                    for row in rows:
                        result_data.append(dict(row))
            except FileNotFoundError:
                return None
        return result_data


class Database:
    def __init__(self):
        self.tables = {}

    def load_data_from_csv(self, table, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader if any(row.values())]

        print(f"Loaded data for {table}:")
        for row in data:
            print(row)

        self.tables[table] = data

    def create_table(self, table, columns):
        self.tables[table] = [{col: None for col in columns}]

    def insert_data(self, table, data):
        if table not in self.tables:
            self.create_table(table, data.keys())

        self.tables[table].append(data)

    def update_table(self, table, condition, new_data):
        for row in self.tables.get(table, []):
            if all(row.get(key) == value for key, value in condition.items()):
                print(f"Updating row: {row}")
                row.update(new_data)
                print(f"Updated row: {row}")


class Table:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def insert(self, entry):
        self.entries.append(entry)

    def update(self, entry_id, key, new_value):
        for entry in self.entries:
            if entry['ID'] == entry_id:
                entry[key] = new_value
                break


csv_file_paths = ['persons.csv', 'login.csv']
csv_reader = CsvReader(file_paths=csv_file_paths)
csv_data = csv_reader.read_csv()

database = Database()

for file_path in csv_file_paths:
    table_name = os.path.splitext(os.path.basename(file_path))[0]
    database.create_table(table_name, [])

for entry_data in csv_data:
    table_name_data = entry_data['ID'].split('_')[0]
    database.insert_data(table_name_data, entry_data)

# Example update
entry_id_to_update = 'some_id'
update_successful = database.update_table('login', {'ID': entry_id_to_update}, {'role': 'student'})
