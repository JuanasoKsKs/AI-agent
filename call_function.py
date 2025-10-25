from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from config import *

def call_function(function_call_part, verbose=False):
    #=================Identify function
    function_name = function_call_part.name
    
    #=================Available functions
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }


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

    #=================Print details with or without verbose
    if verbose:
        print(f"Calling function: {function_call_part.name}({arguments})")
    else:
        print(f" - Calling function: {function_call_part.name}")

        
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