import csv


def write_csv(data, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)


def write_csv_one_col(data, filename):
    write_csv([[item] for item in data], filename)


def read_csv(filename) -> list:
    with open(filename) as f:
        reader = csv.reader(f)
        return list(reader)


def read_csv_one_col(filename) -> list:
    return [row[0] for row in read_csv(filename)]
