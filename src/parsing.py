import os
import json
from parsing_util import is_source_code_file, parse_code_by_language


def extract_functions_from_file(file_path, language, identifier):
    functions = None

    support_language_list = ('c', 'cpp', 'go', 'swift', 'objective-c')
    if language in support_language_list:
        functions = parse_code_by_language(file_path, language, identifier)
    else:
        print(f"{file_path}: Not supported language: {language}")

    return functions


# Function to process a directory and extract functions from source code files
def process_directory(directory_path, identifier):
    function_data = {"data": []}

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            path = file_path.replace(directory_path + '/', '')

            # Skip files with "test" in the path
            if "test" in path:
                continue

            is_source_code, language = is_source_code_file(file_path)
            if is_source_code:
                extracted_functions = extract_functions_from_file(file_path, language, identifier.replace("/", "_"))
                if extracted_functions:
                    function_data['data'].append(
                        {"file_name": path, "language_type": language, "functions": extracted_functions})

    return function_data


# Function to save a dictionary to a JSON file
def save_dict_to_json(data_dict, save_path):
    """
    Save a dictionary to a JSON file.
    Args:
        data_dict (dict): The dictionary to be saved.
        save_path (str): The path to the JSON file where data will be saved.
    """
    with open(save_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)


if __name__ == "__main__":
    repository_dir = "/home/lbs/codedb/target/torvalds_linux/v6.7-rc3/"
    file_functions = process_directory(repository_dir, 'a')
    output_file = 'test.json'
    save_dict_to_json(file_functions, output_file)
    print(f"Function information saved to {output_file}")
