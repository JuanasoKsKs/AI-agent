import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions import *
from config import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    statement = sys.argv
    print("Hello from aiagent!")
    if len(sys.argv) < 2:
        print("Tool usage: uv run main.py <prompt>")
        print("Error: missing prompt", file=sys.stderr)
        print(os.path.join("/home/juenaso/AIagent", "."))
        sys.exit(1)
        return

    user_prompt = statement[1]

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
    model= model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    um = response.usage_metadata
    if len(statement) > 2:
        if statement[2] == "--verbose":
            print("User prompt:", user_prompt)
            print("Prompt tokens:", um.prompt_token_count)
            print("Response tokens:", um.candidates_token_count)


    print(response.text)

if __name__ == "__main__":
    main()
