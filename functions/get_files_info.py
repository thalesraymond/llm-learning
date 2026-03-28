import os


def get_files_info(working_directory, directory="."):

  absolute_working_directory = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(absolute_working_directory, directory))

  is_valid_directory = os.path.isdir(target_dir)

  if not is_valid_directory:
    raise Exception(f'Error: "{directory}" is not a directory')

  common_path = os.path.commonpath([absolute_working_directory, target_dir])

  if common_path != absolute_working_directory:
    raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
  
  files_info = []

  for entry in os.scandir(target_dir):
    name = entry.name
    file_size = entry.stat().st_size
    is_dir = entry.is_dir()
    files_info.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

  return "\n".join(files_info)
