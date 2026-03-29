import os
import subprocess

from functions.path_validation import validate_path_within_working_directory


def run_python_file(working_directory, file_path, args=None):
  try:
    abs_working_dir, absolute_file_path = validate_path_within_working_directory(
        working_directory,
        file_path,
        "execute",
    )

    if not os.path.isfile(absolute_file_path) or not os.access(absolute_file_path, os.R_OK):
        raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
    
    if not file_path.endswith(".py"):
        raise Exception(f'Error: "{file_path}" is not a Python file')
    
    command = ["python", absolute_file_path, *(args or [])]
    
    result = subprocess.run(command, capture_output=True, text=True, cwd=abs_working_dir, timeout=30)

    result_text = "Result of executing Python file:"

    if result.returncode != 0:
      result_text += f'\nProcess exited with code {result.returncode}'

    if result.stdout:
      result_text += f'\nSTDOUT:\n{result.stdout}'

    if result.stderr:
      result_text += f'\nSTDERR:\n{result.stderr}'

    if not result.stdout and not result.stderr:
      result_text += "\nNo output produced by the script."

    return result_text
  except Exception as e:
    return print(f"Error: {e}")