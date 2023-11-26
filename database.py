import csv


class CsvReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        data = []
        with open(self.file_path) as f:
            rows = csv.DictReader(f)
            for r in rows:
                data.append(dict(r))
        return data


class Database:
    def __init__(self):
        self.tables = {}

    def add_table(self, table_name, table_instance):
        self.tables[table_name] = table_instance

    def get_table(self, table_name):
        return self.tables.get(table_name)


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


csv_file_path = 'persons.csv'
csv_reader = CsvReader(file_path=csv_file_path)
persons_data = csv_reader.read_csv()

database = Database()
persons_table = Table(name='persons')

for person in persons_data:
    persons_table.insert(person)

database.add_table('persons', persons_table)

entry_id_to_update = 'some_id'
key_to_update = 'name'
value_to_update = 'John Doe'

# Assuming 'ID' is the key to identify entries
persons_table.update(entry_id_to_update, key_to_update, value_to_update)

# Get the updated data
updated_persons_data = persons_table.entries

