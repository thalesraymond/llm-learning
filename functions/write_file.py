import os
from google.genai import types

from functions.path_validation import validate_path_within_working_directory


def write_file(working_directory, file_path, content):
  try:
    
    _, absolute_file_path = validate_path_within_working_directory(
          working_directory,
          file_path,
          "write",
      )
    
    if os.path.isdir(absolute_file_path):
        raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')

    parent_directory = os.path.dirname(absolute_file_path)
    os.makedirs(parent_directory, exist_ok=True)

    with open(absolute_file_path, "w") as file:
      file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

  except Exception as e:
    return print(f"Error: {e}")


schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes content to a file relative to the working directory, creating parent directories when needed",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the file to write, relative to the working directory",
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="Text content to write into the target file",
      ),
    },
  ),
)