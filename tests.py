from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write import write_file
from functions.run_python_file import run_python_file

test_cases =[
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt")
]


for test_case in test_cases:
    print("-----------------------")
    print(run_python_file(*test_case))