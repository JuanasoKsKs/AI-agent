import os
import sys
import subprocess

def run_python_file(working_directory, file, args=[]):
    try:
        a = sys.argv
        work_path = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(work_path, file))
        if not file_path.startswith(work_path):
            return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File "{file}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file}" is not a Python file.'
        
        command_to_subprocess = ["python", file_path, *args]

        #it returns a CompletedProcess object with:
        #returncode: exit code (0 is success)
        #stdout: captured standard output
        #stderr: captured standard error
        CompletedProcess = subprocess.run(
            command_to_subprocess,
            cwd=work_path, 
            capture_output=True, #equal as using: stdout=True, stderr=True = it returns both
             
           
            timeout=30, #kills the process if running for this time (in seconds)
            text=True, #set if the outputs are in strings or bytes
        )
        out = CompletedProcess.stdout.strip()
        err = CompletedProcess.stderr.strip()

        if not out and not err:
            return "No output produced."

        parts = []
        if out:
            parts.append(f"STDOUT:\n{out}")
        if err:
            parts.append(f"STDERR:\n{err}")
        if CompletedProcess.returncode != 0:
            parts.append(f"Process exited with code {CompletedProcess.returncode}")

        return "\n".join(parts)

    except Exception as e:
        return f'Error: executing Python file: {e}'