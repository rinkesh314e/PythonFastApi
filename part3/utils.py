import json

def read_json():
    try:
        with open('./data/data_dict.json', 'r') as file:
            healthcare_providers = json.load(file)
    except IOError:
        healthcare_providers = {}
    return healthcare_providers


def write_json(healthcare_providers):
    try:
        with open('./data/data_dict.json', 'w+') as file:
            json.dump(healthcare_providers, file)
    except IOError as err:
        print(f'Error: {err}')