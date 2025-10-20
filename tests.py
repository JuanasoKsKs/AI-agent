from functions import *

test_cases =[
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does not exist.py"),
    ("calculator", "lorem.txt")
]


for test_case in test_cases:
    print(get_file_content(*test_case))