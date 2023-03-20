import pytest
import jsonschema
import json
import os

print(os.getcwd())


def load_json_file(path):
    with open(path) as f:
        obj = json.load(f)
    return obj


schema_path = './schema/default_schema.json'

pass_tests = ['test_cases/correct_a.json', 'test_cases/correct_b.json',
              'test_cases/correct_c.json', 'test_cases/correct_d.json']
fail_tests = ['test_cases/wrong_a.json', 'test_cases/wrong_b.json', 
              'test_cases/wrong_c.json']


schema = load_json_file(schema_path)


def validate_json(filename):
    """REF: https://json-schema.org/ """
    json_data = load_json_file(filename)
    jsonschema.validate(instance=json_data, schema=schema)


def get_json_files_in_dir(dir):
    all_json_files = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith((".json")):
                all_json_files.append((root + '/' + name)[2:])
    return all_json_files


@pytest.mark.parametrize("filename", pass_tests)
def test_correct_cases(filename):
    validate_json(filename)


@pytest.mark.parametrize("filename", fail_tests)
def test_wrong_cases(filename):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate_json(filename)


all_files = get_json_files_in_dir('./parse')


@pytest.mark.parametrize("filename", all_files)
def test_file(filename):
    validate_json(filename)


@pytest.mark.parametrize("filename", all_files)
def test_dataset_name_is_correct(filename):
    json_data = load_json_file(filename)
    dataset_name = json_data.get('table', {}).get('dataset_name', None)
    assert os.path.split(filename)[0].split("/")[-1] == dataset_name


@pytest.mark.parametrize("filename", all_files)
def test_table_name_is_correct(filename):
    json_data = load_json_file(filename)
    table_name = json_data.get('table', {}).get('table_name', None)
    basename = os.path.basename(filename)
    expected_table_name = basename.replace('.json', '')
    assert expected_table_name == table_name
