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
        "DISPLACEMENT_Z": And(list, lambda l: len(l) > 0, [Use(float)])
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

def validate_yaml_file(yaml_path):

    with open(yaml_path, 'r') as f:
        meta = yaml.safe_load(f)

    required_keys = ["name", "test_description", "json_file", "date", "stem_version"]
    for key in required_keys:
        if key not in meta:
            raise ValueError(f"Missing required metadata field: {key}")

    return meta


if __name__ == "__main__":
    print(json_validator("tests/data/json_output_80_length.json"
                   ))
