import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):

    real_working_dir = os.path.realpath(working_directory)
    full_file_path = os.path.realpath(os.path.join(working_directory, file_path))
    
    if not full_file_path.startswith(real_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    
    '''
    read the file contents as a string, to prevent burning through LLM tokens, ensure we have a max limit of 10000 characters
    if the file is greater than 10000 characters, truncate it
    '''

    try:
        with open(full_file_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_file_path) > MAX_CHARS:
                file_content_string = file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f'Error: {e}'

    return file_content_string


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="read the contents of a file in a specified directory and return the content of the file as a string, if the file is greater than MAX_CHARS currently 10000 it is truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""
                The file path where the file we want to read and return the contents of files, 
                large files > than MAX_CHARS are trucated, e.g. 10000 characters will be the truncation limit if MAX_CHARS=10000
                """,
            ),
        },
    ),
)
