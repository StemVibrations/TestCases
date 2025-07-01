from scripts.validators import json_validator, yaml_validator, mdpa_validator


def test_json_validator():
    """
    Test with a valid JSON file
    """
    assert json_validator("tests/data/json_output_80.json", "1.2.3")
    assert json_validator("tests/data/json_output_120.json", "1.2.3")

    assert json_validator("tests/data/json_output_80_alpha.json", "1.2.4.a")


def test_json_validator_wrong_version(capsys):
    """
    Test with a valid JSON file and wrong version
    """

    # Call the function with a non-existent file
    result = json_validator("tests/data/json_output_80.json", "1.2.5")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the function returns False
    assert not result

    # Assert that the printed message contains "file not found"
    assert "Unsupported STEM version: 1.2.5" in captured.out


def test_json_validator_file_not_found(capsys):
    """
    Test the json_validator function with a non-existent file.
    """
    # Call the function with a non-existent file
    result = json_validator("tests/data/non_existent_file.json", "1.2.3")

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
    # Call the function
    result = json_validator("tests/data/json_output_80_length.json", "1.2.3")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Length mismatch in NODE_76: TIME=149"
    "VELOCITY_X=150 VELOCITY_Y=150 VELOCITY_Z=150"
    "Length mismatch found in displacement data." in captured.out

def test_yaml():
    """
    Test the yaml_validator
    """

    # Call the function
    assert yaml_validator("tests/data/case_1.yaml")

def test_yaml_empty_value(capsys):
    """
    Test the yaml_validator
    """

    # Call the function
    result = yaml_validator("tests/data/case_1_empty.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Metadata field 'test-description' is empty." in captured.out

def test_yaml_missing_key(capsys):
    """
    Test the yaml_validator with a missing key
    """

    # Call the function
    result = yaml_validator("tests/data/case_1_missing.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Missing required metadata field: date" in captured.out

def test_yaml_no_json(capsys):
    """
    Test the yaml_validator with a non existing json
    """

    # Call the function
    result = yaml_validator("tests/data/case_1_no_json.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "JSON file json_output.json does not exist." in captured.out


def test_json_size_zero(capsys):
    """
    Test the yaml_validator
    """

    # Call the function
    result = yaml_validator("tests/data/case_1_json_empty.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "JSON file json_output_empty.json is empty." in captured.out

def test_input_size_zero(capsys):
    """
    Test the yaml_validator with an input file size of zero
    """

    # Call the function
    result = yaml_validator("tests/data/case_1_input_empty.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "Input file input_empty.py is empty." in captured.out

def test_yaml_not_existing(capsys):
    """
    Test the yaml_validator with an yaml file that does not exist
    """

    # Call the function
    result = yaml_validator("case10.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "YAML file case10.yaml does not exist." in captured.out

def test_yaml_zero_size(capsys):
    """
    Test the yaml_validator with an yaml file that does not exist
    """

    # Call the function
    result = yaml_validator("tests/data/empty.yaml")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "YAML file tests/data/empty.yaml is empty." in captured.out


def test_mdpa():
    """
    Test the yaml_validator with an mdpa file
    """

    # Call the function
    assert mdpa_validator("tests/data/example.mdpa")


def test_mdpa_not_existing(capsys):
    """
    Test the yaml_validator with an mdpa file that does not exist
    """

    # Call the function
    result = mdpa_validator("tests/data/mdpa.mdpa")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "MDPA file tests/data/mdpa.mdpa does not exist." in captured.out


def test_mdpa_size(capsys):
    """
    Test the mpda_validator with an mdpa file that does not exist
    """

    # Call the function
    result = mdpa_validator("tests/data/empty.mdpa")

    # Capture the printed output
    captured = capsys.readouterr()

    assert not result

    # Assert that the printed message is correct
    assert "MDPA file tests/data/empty.mdpa is empty." in captured.out

