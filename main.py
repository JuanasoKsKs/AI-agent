import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import *
from call_function import call_function




def main():
    load_dotenv()

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
        print('Usage: python main.py "prompt" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    #=================Client generation
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    #================Creation of first Message
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        #================Response from Client ==== Generate Content
        response = generate_content(client, model_name, messages)
        count = 1
        
        while  response.function_calls and count < 15:
            count +=1

            for candidate in response.candidates:
                messages.append(candidate.content)

            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                resp = function_call_result.parts[0].function_response.response
                if "result" not in  resp:
                    raise RuntimeError("Tool response missing 'result'")
                new_message = resp["result"]
                messages.append(
                    types.Content(role="user", parts=[types.Part(text=new_message)])
                )

            response = generate_content(client, model_name, messages)
          
        #================Usage of Metadata
        um = response.usage_metadata
        if verbose:
            print("\nUser prompt:", user_prompt)
            print("Prompt tokens:", um.prompt_token_count)
            print("Response tokens:", um.candidates_token_count,"\n")

        print(response.text)

    except Exception as e:
        print(e)



def generate_content(client, model_name, messages):
    return  client.models.generate_content(
        model= model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            )
        )




if __name__ == "__main__":
    main()
