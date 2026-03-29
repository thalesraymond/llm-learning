import os

from config import MAX_CHARACTERS
from functions.path_validation import validate_path_within_working_directory



def get_file_content(working_directory, file_path):
    try:
      _, absolute_file_path = validate_path_within_working_directory(
          working_directory,
          file_path,
          "read",
      )
      
      if not os.path.isfile(absolute_file_path) or not os.access(absolute_file_path, os.R_OK):
          raise Exception(f'Error: File not found or is not a regular file: "{file_path}"') 

      with open(absolute_file_path, 'r') as file:
          file_content = file.read(1000)

          if file.read(1):
              file_content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
          return file_content
    except Exception as e:
      return print(f"Error: {e}")