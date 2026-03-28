import os

from config import MAX_CHARACTERS



def get_file_content(working_directory, file_path):
    try:
      absolute_working_directory = os.path.abspath(working_directory)
      absolute_file_path = os.path.join(absolute_working_directory, file_path)

      common_path = os.path.commonpath([absolute_working_directory, absolute_file_path])
      
    #   print(absolute_working_directory)
    #   print(absolute_file_path)
    #   print(common_path)

      if common_path != absolute_working_directory:
          raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
      
      if not os.path.isfile(absolute_file_path) or not os.access(absolute_file_path, os.R_OK):
          raise Exception(f'Error: File not found or is not a regular file: "{file_path}"') 

      with open(absolute_file_path, 'r') as file:
          file_content = file.read(1000)

          if file.read(1):
              file_content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
          return file_content
    except Exception as e:
      return print(f"Error: {e}")