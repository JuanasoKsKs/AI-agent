import os

def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        relative_directory = os.path.join(working_directory, directory)
        full_path = os.path.abspath(relative_directory)
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        files = os.listdir(full_path)
        files_with_description = []
        for file in files:
            file_size = os.path.getsize(os.path.join(full_path, file))
            is_dir = os.path.isdir(os.path.join(full_path, file))
            files_with_description.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_with_description)
    except Exception as e:
        return f"Error: {e}"
