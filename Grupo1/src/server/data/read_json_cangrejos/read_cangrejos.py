import json

def read_cangrejos(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)