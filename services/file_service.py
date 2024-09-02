def load_json_file(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)
