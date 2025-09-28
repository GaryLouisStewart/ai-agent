import os
from google.genai import types

def write_file_content(working_directory, file_path, content):
    real_working_dir = os.path.realpath(working_directory)
    full_file_path = os.path.realpath(os.path.join(working_directory, file_path))

    if not full_file_path.startswith(real_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # try and create the file and write to it, if it doesn't already exist otherwise just try and write to the file.

    try:
        # check and see if the path to our directory we specify exists. if not create these directories. 
        if not os.path.exists(os.path.dirname(full_file_path)):
            os.makedirs(os.path.dirname(full_file_path)) 
        # Now begin creating and writing to the file.
        with open(full_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f'Error: Reason: {e}'


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description= """
        write to a specified file, if the file doesn't already exist then create it, otherwise just write to the file.
        only allows writing to files within the permitted working directory, if file falls outside, throws an error and blocks writing.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""
                The file path where the file we want to write to exists. If the file doesn't exist then it will be created.
                if the file path falls outside permitted working dir, do not write to it.
                """,
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="""
                the content to add into the file. represented as a string. 
                """,
            ),
        },
    ),
)
