import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python import schema_run_python
from functions.write_file_content import schema_write_file_content
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    if not args:
        print("AI code Assist")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a portfolio website?"')
        sys.exit(1)

    # store the prompts we pass as a list of messages, this will later be used to keep track of the entire conversation we have with the LLM
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    # only allows our function to be called a maximum of 20 times.
    count = 0

    while count <= 20:
        count += 1
        try:
            result = generate_content(client, messages, verbose)
            if result:
                print("Final response:")
                print(result)
                break
        except Exception as e:
            print(f"Error: {e}")
            break


def generate_content(client, messages, verbose):
    system_prompt = """
    You are an AI programming agent designed to be helpful.

    When you are asked a question by a user, you should ALWAYS start by exploring the codebase using your available tools before providing an answer. You are able to perform the following operations:
    
    - List files and directories (use this firstly to understand the project structure)
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    Start by listing the files to understand what code is available, then read relevant files to answer the user's question.

    All paths you provide should be relative to the working directory. You won't need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    model_name = "gemini-2.0-flash-001"

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python,
            schema_write_file_content,
        ]
    )

    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    
    # iterate over .candiate and add it's responses to the messages list
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # use this to store the function responses
    function_responses =[]

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if getattr(part, "function_call", None):
                function_call_result = call_function(part.function_call, verbose=verbose)
                if (
                    not function_call_result.parts
                    or not getattr(function_call_result.parts[0], "function_response")
                ):
                    raise RuntimeError("Tool called returned no function_response")

                #collect the response part
                function_responses.append(function_call_result.parts[0])
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}") 

    if function_responses:
        messages.append(types.Content(role="user", parts=function_responses))

    if function_responses:
        return None
    else:
        return response.text




if __name__ == "__main__":
    main()
