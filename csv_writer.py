import csv
import os

class CsvWriter:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CsvWriter, cls).__new__(cls)
        return cls.instance

    def write(self, data, file_path, labels, item_to_row_func=None, overwrite=False, file_open_mode="w"):
        file_name = f"{file_path}.csv"
        if not os.path.exists(file_name) and file_open_mode=="a":
            file_open_mode = "w"

        if not overwrite and file_open_mode != "a":
            result_id = 0
            while os.path.exists(file_name):
                result_id += 1
                file_name = f"{file_path}{result_id}.csv"

        with open(file_name, mode=file_open_mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=labels)
            if file_open_mode == "w":
                writer.writeheader()
            for row in data:
                if item_to_row_func is not None:
                    row = item_to_row_func(row)
                writer.writerow(row)

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=";")
            for line in reader:
                result.append(line)
        return result

if __name__ == '__main__':
    result = CsvWriter().read("../partial_results/community.csv")