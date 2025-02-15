import csv
import json
def make_json(csvFilePath):
    
    # create a dictionary
    data = {}
    
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            
            key = rows['Exporter Details']
            data[key] = rows


    return data
        