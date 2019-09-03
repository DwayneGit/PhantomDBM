import json

def validateJsonScript(parent, json_str):
    try:
        return json.loads(json_str)
    except json.decoder.JSONDecodeError as err:
        raise
