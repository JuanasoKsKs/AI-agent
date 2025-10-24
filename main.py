import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file




def main():
    load_dotenv()

    statement = sys.argv
    #===============Verbose and Arguments
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    #===============Error if missing Prompt
    if not args:
        print("AI Code Assistant")
        print("Error: missing prompt", file=sys.stderr)
        print('\nUsage: python main.py "prompt" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    #=================Client generation
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    #================Messages
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    #================Response from Client
    response = client.models.generate_content(
    model= model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
        )
    )

    #================Usage of Metadata
    um = response.usage_metadata

    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", um.prompt_token_count)
        print("Response tokens:", um.candidates_token_count)

    
    try:
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
    except Exception as e:
        print(e)

def call_function(function_call_part, verbose=False):
    #=================Print details with or without verbose
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    #=================Available functions
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    #=================Identify function
    function_name = function_call_part.name

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    #================add working directory to arguments that are to be sent to the function    
    arguments = function_call_part.args
    arguments["working_directory"] = working_dic #directory imported from config.py

    function_result = functions[function_name](**arguments)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )





if __name__ == "__main__":
    main()
