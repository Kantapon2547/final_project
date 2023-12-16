import csv


class CsvReader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def read_csv(self):
        result_data = []
        for file_paths in self.file_paths:
            try:
                with open(file_paths) as csv_file:
                    rows = csv.DictReader(csv_file)
                    for row in rows:
                        result_data.append(dict(row))
            except FileNotFoundError:
                return None
        return result_data


class Database:
    def __init__(self):
        self.tables = {}

    def add_table(self, table, table_instances):
        self.tables[table] = table_instances

    def get_table(self, table):
        return self.tables.get(table)

    def create_table(self, table):
        new_table = Table(name=table)
        self.add_table(table, new_table)

    def update_table(self, table, data):
        tables = self.get_table(table)
        if tables:
            tables.update(data)
        else:
            return None

    def insert_data(self, table, data):
        table = self.get_table(table)
        if table:
            table.insert(data)
        else:
            return None


class Table:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def insert(self, entry):
        self.entries.append(entry)

    def update(self, entry_id, key, new_value):
        for entry in self.entries:
            if entry.get('ID') == entry_id:
                entry[key] = new_value
                break


# Read data from CSV and insert into a table
csv_file_paths = ['persons.csv', 'login.csv']
csv_reader = CsvReader(file_paths=csv_file_paths)
csv_data = csv_reader.read_csv()

# Create a database and tables
database = Database()

for file_path in csv_file_paths:
    table_name = file_path.split('.')[0]  # Extract table name from file path
    table_instance = Table(name=table_name)
    database.add_table(table_name, table_instance)


# Insert data into the tables
for entry_data in csv_data:
    table_name_data = entry_data['ID'].split('_')[0]  # Extract table name from ID
    database.insert_data(table_name_data, entry_data)

# Example update
table_to_update = 'persons'
entry_id_to_update = 'some_id'
key_to_update = 'name'
value_to_update = 'John Doe'

# Assuming 'ID' is the key to identify entries
update_successful = database.tables[table_to_update].update(entry_id_to_update, key_to_update, value_to_update)
