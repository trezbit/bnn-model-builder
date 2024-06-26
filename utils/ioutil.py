'''I/O utility functions for the BrainNet modules.'''


import json
import csv




def load_json_to_dict(arraykey, dictkey, filename):
    '''Load and build node dictionary from a JSON'''
    dict = {}
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data[arraykey]:
                dict[item[dictkey]] = item
    except Exception as e:
        print("Error: ", e, "File: ", filename)
        return None
    return dict

def write_dict_to_json(dict, filename):
    '''Write a dictionary to a JSON file'''
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4)
    return

def graph_jsondata_to_csv(arraykey,injson,outcsv):
    '''Convert JSON data to CSV'''
    print("Converting JSON data to CSV: ", injson, " to ", outcsv, ", array key: ", arraykey)
    with open(injson) as json_file:
        jsondata = json.load(json_file)

    data_file = open(outcsv, 'w', newline='')
    csv_writer = csv.writer(data_file,quoting=csv.QUOTE_NONNUMERIC,doublequote=True)

    count = 0
    for data in jsondata[arraykey]:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())

    data_file.close()
    return

def write_array_to_csv(data, header, filename):
    '''Write an array to a CSV file'''
    with open(filename
                , mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)        
    return



# Function to read a JSON file into a dictionary

def read_json_to_dict(filename):
    '''Read a JSON file into a dictionary'''
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Function to read a csv to an array of dictionaries

def read_csv_to_dict(filename):
    '''Read a CSV file into an array of dictionaries'''
    with open(filename, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = []
        for row in reader:
            if row is not None and len(row) > 0:
                data.append(row)
    return data
