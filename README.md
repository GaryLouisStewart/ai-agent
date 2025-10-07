# AI Agent

This is an ai agent that I built in collaboration with boot.dev whilst doing their ai-gent in python course. 
The intent is to demostrate, how to create an agent that can operate on files within the file-system, securely and refactor buggy python programs.

This uses the gemini model in order to perform an analysis of the prompts that it is given, and it acts as a programming assistant.

## Features

*   uses googles 'gemini-2.0-flash-001' model in order to be able to prompt and return information from gemini.
*   ability to look at file content and return it
*   get file information, files in a specific directory and their sizes
*   write_file_content, ability to update & edit files.
*   call functions that we define in our functions folder, this makes our agent easily extensible in future.

## Usage

To use the ai-agent, run `main.py` with the expression as a command-line argument:

```bash
$ uv run main.py

This will output:
```

```bash

AI code Assist

Usage: python main.py "your prompt here" [--verbose]
Example: python main.py "How do I build a portfolio website?"
```

## Files

*   `main.py`: The main entry point of the application.
*   `functions`: The folder containing the functions the Agent can carry out.
*   `test_*.py`: these are the files I created to test out our AI Agent.
*   `call_function.py`: this is used to map the functions that the AI Agent can call, to help when we prompt it.
*   `calculator`: This is the folder we created as an example to show how it can operate in the real world. it contains a simple calculator application, that we can get the agent to act on.

## Running Tests

To run the unit tests, execute the `tests.py` file:

```bash
uv run test_call_function.py
```

