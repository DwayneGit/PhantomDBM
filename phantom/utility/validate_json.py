import json

def validate_json_script(parent, json_str):
    try:
        return json.loads(json_str)
    except json.decoder.JSONDecodeError as err:
        raise
