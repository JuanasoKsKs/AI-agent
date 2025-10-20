import os

def write_file(working_directory, file_path, content):
    try:

        abs_work = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(abs_work, file_path))
        if not abs_path.startswith(abs_work + os.sep):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{abs_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"