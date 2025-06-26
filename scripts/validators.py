import os
import json
from schema import Schema, And, Use, SchemaError, Regex
import yaml



def __definitions() -> Schema:
    """
    Defines the configuration schema for the validation of the input json file

    return: Schema configuration file
    """

    conf_schema_node = Schema({
        "COORDINATES": And(list, lambda l: len(l) == 3, [Use(float)]),
        "DISPLACEMENT_X": And(list, lambda l: len(l) > 0, [Use(float)]),
        "DISPLACEMENT_Y": And(list, lambda l: len(l) > 0, [Use(float)]),
        "DISPLACEMENT_Z": And(list, lambda l: len(l) > 0, [Use(float)]),
        "VELOCITY_X": And(list, lambda l: len(l) > 0, [Use(float)]),
        "VELOCITY_Y": And(list, lambda l: len(l) > 0, [Use(float)]),
        "VELOCITY_Z": And(list, lambda l: len(l) > 0, [Use(float)]),
        "ACCELERATION_X": And(list, lambda l: len(l) > 0, [Use(float)]),
        "ACCELERATION_Y": And(list, lambda l: len(l) > 0, [Use(float)]),
        "ACCELERATION_Z": And(list, lambda l: len(l) > 0, [Use(float)]),
    })

    conf_schema_json = Schema({
        "TIME": And(list, lambda l: len(l) > 0, [Use(float)]),
        Regex(r'^NODE_\d+$'): conf_schema_node,
    })

    return conf_schema_json

def __check_lenghts(data: dict) -> bool:
    """
    Checks if the lengths of TIME and displacement arrays are consistent across all nodes.

    Parameters:
        data (dict): Parsed JSON data.
    Returns:
        bool: True if lengths are consistent, False if mismatches found.
    """

    time_len = len(data["TIME"])
    for key, value in data.items():
        if key.startswith("NODE_"):
            dx = len(value["DISPLACEMENT_X"])
            dy = len(value["DISPLACEMENT_Y"])
            dz = len(value["DISPLACEMENT_Z"])

            if not (dx == dy == dz == time_len):
                print(f"Length mismatch in {key}: "
                      f"TIME={time_len}"
                      f"DISPLACEMENT_X={dx}",
                      f"DISPLACEMENT_Y={dy}",
                      f"DISPLACEMENT_Z={dz}")
                return False
    return True


def json_validator(json_path: str) -> bool:
    """
    Validates a JSON file against expected structure and displacement length consistency.

    Parameters:
        json_path (str): Path to the JSON file.

    Returns:
        bool: True if valid, False if errors found.
    """
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return False

    conf_schema = __definitions()
    try:
        conf_schema.validate(data)
    except SchemaError as e:
        print(f"Schema validation error: {e}")
        return False

    # Custom cross-field validation
    if __check_lenghts(data) == False:
        print("Length mismatch found in displacement data.")
        return False
    return True


def yaml_validator(yaml_path: str) -> bool:
    """
    Validates a YAML file for required metadata fields.

    Parameters:
        yaml_path (str): Path to the YAML file.
    Returns:
        bool: True if valid, False if required fields are missing.
    """

    # check if yaml file exists and size is greater than 2 bytes
    if not os.path.isfile(yaml_path):
        print(f"YAML file {yaml_path} does not exist.")
        return False
    if os.path.getsize(yaml_path) <= 2:
        print(f"YAML file {yaml_path} is empty.")
        return False

    # yaml directory
    yaml_dir = os.path.dirname(yaml_path)

    # load yaml file
    with open(yaml_path, 'r') as f:
        meta = yaml.safe_load(f)

    required_keys = ["name", "title", "test-description","date", "json-file", "input-file", "STEM-version"]
    # check if all required keys are present
    for key in required_keys:
        if key not in meta:
            print(f"Missing required metadata field: {key}")
            return False

    # check if all keys are not empty
    for key, value in meta.items():
        if not value:
            print(f"Metadata field '{key}' is empty.")
            return False

    # check is json-file and input files exist and size is greater than 2 bytes
    if not os.path.isfile(os.path.join(yaml_dir, meta["json-file"])):
        print(f"JSON file {meta['json-file']} does not exist.")
        return False
    if os.path.getsize(os.path.join(yaml_dir, meta["json-file"])) <= 2:
        print(f"JSON file {meta['json-file']} is empty.")
        return False
    if not os.path.isfile(os.path.join(yaml_dir, meta["input-file"])):
        print(f"Input file {meta['input-file']} does not exist.")
        return False
    if os.path.getsize(os.path.join(yaml_dir, meta["input-file"])) <= 2:
        print(f"Input file {meta['input-file']} is empty.")
        return False

    return True
