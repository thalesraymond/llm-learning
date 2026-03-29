import os

from functions.path_validation import validate_path_within_working_directory


def get_files_info(working_directory, directory="."):
  try:
    _, target_dir = validate_path_within_working_directory(
      working_directory,
      directory,
      "list",
    )

    is_valid_directory = os.path.isdir(target_dir)

    if not is_valid_directory:
      raise Exception(f'Error: "{directory}" is not a directory')

    files_info = []

    for entry in os.scandir(target_dir):
      name = entry.name
      file_size = entry.stat().st_size
      is_dir = entry.is_dir()
      files_info.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(files_info)
  except Exception as e:
    return print(f"Error: {e}")


