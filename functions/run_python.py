import os
import subprocess
from google.genai import types

def run_python(working_directory, file_path, args=None):
    # use a safe default of None, and then normalise inputs.
    if args is None:
        args = []
    else:
        if isinstance(args, str):
            import shlex
            args = shlex.split(args)
    
    real_working_dir = os.path.realpath(working_directory)
    full_file_path = os.path.realpath(os.path.join(working_directory, file_path))

    if not full_file_path.startswith(real_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'
    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        if len(args) == 0:
            print(type(args))
            completed_process = subprocess.run(["python", full_file_path], cwd=real_working_dir, capture_output=True, timeout=30)
        else:
            print(type(args))
            completed_process = subprocess.run(["python", full_file_path] + args, cwd=real_working_dir, capture_output=True, timeout=30)
        
        stdout_str = completed_process.stdout.decode('utf-8').strip()
        stderr_str = completed_process.stderr.decode('utf-8').strip()
        
        if not stdout_str and not stderr_str:
            return 'No output produced.'

        # create a conditional output string, based on the above if statement being false.
        output_parts = []
        if stdout_str:
            output_parts.append(f'STDOUT: {stdout_str}')
        if stderr_str:
            output_parts.append(f'STDERR: {stderr_str}')
        
        if completed_process.returncode != 0:
           output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        return "\n".join(output_parts)

    except subprocess.SubprocessError as e:
        return f"Error: executing Python file: {e}"


schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="""
        run a python file provided with the full path, optionally specify arguments for the python file, 
        if args is empty execute the file without them
        """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""
                The file path where the file we want to run is located. This is constrained to the working directory
                if the file path falls outside of this working directory it is not allowed to execute.
                if the file is not a python file, do not execute it.
                """,
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="""
                optional: the arguments to pass to the python file
                this is a list that is passed to the function containing all the arguments you wish to pass to the file
                """,
            ),
        },
    ),
) 
