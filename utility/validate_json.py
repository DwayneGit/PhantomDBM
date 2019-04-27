import json

def validate_json_script(json_str):
    try:
        json.loads(json_str)
    except json.decoder.JSONDecodeError:
        raise
    return json_str