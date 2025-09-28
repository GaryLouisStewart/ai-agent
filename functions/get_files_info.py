import os
from google.genai import types

def get_files_info(working_directory, directory="."):
	# creates a full path to the directory
    real_working_dir = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(real_working_dir, directory))

    # if the full path is outside the working directory, then return an error,
    # the LLM should never be able to perform tasks outside the working directory we assign to it.
    if not full_path.startswith(real_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    file_list = []
    
    try:
      for file in os.listdir(path=full_path):
          full_file_path = os.path.join(full_path, file)
          file_size = os.path.getsize(full_file_path)
          is_dir = os.path.isdir(full_file_path)
          file_list.append(f' - {file}: file_size={file_size} bytes, is_dir={is_dir}')
    except Exception as e:
        return f'Error: {e}'

    return "\n".join(file_list)



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their respective sizes, constrained to the working directory only.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to working dir, if not provided, lists files within the working dir itself.",
            ),
        },
    ),
)
