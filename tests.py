from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write import write_file

test_cases =[
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


for test_case in test_cases:
    print(write_file(*test_case))