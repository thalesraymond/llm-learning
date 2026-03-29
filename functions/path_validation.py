import os


def validate_path_within_working_directory(working_directory, path, action):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_target_path = os.path.abspath(os.path.join(absolute_working_directory, path))

    common_path = os.path.commonpath([absolute_working_directory, absolute_target_path])

    if common_path != absolute_working_directory:
        raise Exception(
            f'Error: Cannot {action} "{path}" as it is outside the permitted working directory'
        )

    return absolute_working_directory, absolute_target_path
