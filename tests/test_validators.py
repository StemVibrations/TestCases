from scripts.validators import json_validator, yaml_validator


def test_json_validator():
    """
    Test with a valid JSON file
    """
    assert json_validator("tests/data/json_output_80.json")
    assert json_validator("tests/data/json_output_120.json")

def test_json_validator_file_not_found(capsys):
    """
    Test the json_validator function with a non-existent file.
    """
    # Call the function with a non-existent file
    result = json_validator("tests/data/non_existent_file.json")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the function returns False
    assert not result

    # Assert that the printed message contains "file not found"
    assert "No such file or directory" in captured.out


def test_json_validator_invalid_json(capsys):
    """
    Test the json_validator function with an invalid JSON file.
    """
    # Call the function with an invalid JSON file
    result = json_validator("tests/data/json_output_80_length.json")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Length mismatch in NODE_76: TIME=149"
    "DISPLACEMENT_X=150 DISPLACEMENT_Y=150 DISPLACEMENT_Z=150"
    "Length mismatch found in displacement data." in captured.out

def test_yaml():
    """
    Test the yaml_validator
    """

    # Call the function with an invalid JSON file
    assert yaml_validator("tests/data/case_1.yaml")

def test_yaml_empty_value(capsys):
    """
    Test the yaml_validator
    """

    # Call the function with an invalid JSON file
    result = yaml_validator("tests/data/case_1_empty.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Metadata field 'test-description' is empty." in captured.out

def test_yaml_missing_key(capsys):
    """
    Test the yaml_validator
    """

    # Call the function with an invalid JSON file
    result = yaml_validator("tests/data/case_1_missing.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Missing required metadata field: date" in captured.out
