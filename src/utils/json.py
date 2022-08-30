import json


def js_to_json(filename):
    with open(filename) as f:
        f.readline()
        f.seek(f.tell() - 2)
        return json.load(f)


def pretty_dump(obj, filename, *args, **kwargs):
    with open(filename, 'w') as f:
        json.dump(obj, f, *args, indent=4, **kwargs)
