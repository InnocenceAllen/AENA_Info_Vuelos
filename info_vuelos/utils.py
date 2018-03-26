import csv


def createCSV(filename,data):
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(map(lambda x: [x], data))