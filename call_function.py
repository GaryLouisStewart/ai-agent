from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file_content import write_file_content
from functions.run_python import run_python


FUNCTIONS_MAP = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file_content": write_file_content,
        "run_python": run_python,
}


def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    

    function_name = function_call_part.name
    func = FUNCTIONS_MAP.get(function_name)
    
    if func is None:
        return types.Content(
           role="tool",
           parts=[
               types.Part.from_function_response(
               name=function_name,
               response={"error": f"Unknown function: {function_name}"},
               )
          ],
        )
    else:
        args = dict(function_call_part.args)
        args["working_directory"] = "./calculator"
        
        function_result = func(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ]
        )


