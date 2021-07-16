import json

_DATABASE_JSON = "./data/data_dict.json"

def read_json():
    try:
        with open(_DATABASE_JSON, 'r') as file:
            healthcare_providers = json.load(file)
    except IOError:
        healthcare_providers = {}
    return healthcare_providers


def write_json(healthcare_providers):
    try:
        with open(_DATABASE_JSON, 'w+') as file:
            json.dump(healthcare_providers, file)
    except IOError as err:
        print(f'Error: {err}')


def get_items(healthcare_providers: dict ,skip: int =0, limit: int = 10):
    result = {}
    for i, data in enumerate(healthcare_providers.items()):
        if i>=skip and i<skip+limit:
            k,v = data
            result[k] = v
    return result