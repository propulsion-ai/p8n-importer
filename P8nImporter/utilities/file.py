import os
import json

# Load JSON file
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


def generate_search_paths(full_path, source_path):
    """
    Generate a list of search paths by combining segments of the full path with the source path.

    Args:
        full_path (str): The full path from which to generate search paths.
        source_path (str): The source path to combine with segments of the full path.

    Returns:
        list: A list of search paths generated by combining segments of the full path with the source path.
    """
    full_path_parts = os.path.dirname(full_path).split(os.sep)
    source_path_parts = source_path.split(os.sep)

    search_paths = set()

    # Iterate over segments of full path and combine with source path
    for i in range(len(source_path_parts)):
        for j in range(len(full_path_parts)):
            combined_path = os.path.join(*source_path_parts[:i], *full_path_parts[j:])
            search_paths.add(combined_path)

    search_paths.add(source_path)
    return list(search_paths)

def find_file(full_path, source_path):
    """
    Find the file with the given full path in the specified source path or its parent directories.

    Args:
        full_path (str): The full path of the file to find.
        source_path (str): The source path to search for the file.

    Returns:
        str or None: The path of the found file, or None if the file is not found.
    """
    filename = os.path.basename(full_path)
    search_paths = generate_search_paths(full_path, source_path)

    # Search for the file in the generated paths
    for path in search_paths:
        potential_path = os.path.join(path, filename)
        if os.path.isfile(potential_path):
            return potential_path

    return None