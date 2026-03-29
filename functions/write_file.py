import os

from functions.path_validation import validate_path_within_working_directory


def write_file(working_directory, file_path, content):
  try:
    
    abs_working_dir, absolute_file_path = validate_path_within_working_directory(
          working_directory,
          file_path,
          "write",
      )
    
    if os.path.isdir(absolute_file_path):
        raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')

  except Exception as e:
    return print(f"Error: {e}")