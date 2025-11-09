def serialize_json(data):
    import json
    return json.dumps(data)

def deserialize_json(json_string):
    import json
    return json.loads(json_string)

def save_json_to_file(data, file_path):
    import json
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def load_json_from_file(file_path):
    import json
    with open(file_path, 'r') as json_file:
        return json.load(json_file)