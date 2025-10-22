# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

test_cases =[
    ("calculator", "main.py", ['2 + 5']),
]


for test_case in test_cases:
    print("-----------------------")
    print(run_python_file(*test_case))