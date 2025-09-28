import unittest
import os
from functions.get_file_content import get_file_content
from config import MAX_CHARS

class TestFileContent(unittest.TestCase):

    def _get_expected_output(self, working_directory, file_path, max_chars):
        """
        generates the expected string output for a given file, applying
        truncation logic if the file size exceeds max_chars

        Args:
            working_directory (str): The base directory for the operation.
            file_path (str): The relative path to the file
            max_chars (int): The character limit for truncation
    Returns:
            str: The expected content string
        """
        full_path = os.path.join(working_directory, file_path)
        file_size = os.path.getsize(full_path)

        if file_size > max_chars:
            with open(full_path, 'r') as f:
                content = f.read(max_chars)
            truncation_message = f'[...File "{file_path}" truncated at {max_chars} characters]'
            return content + truncation_message
        else:
            with open(full_path, 'r') as f:
                return f.read()


    def test_main_py(self):
        # read file contents into a variable
        file_content = self._get_expected_output("calculator", "main.py", MAX_CHARS)
        self.assertEqual(get_file_content("calculator", "main.py"), file_content)

    def test_pkg_calculator(self):
        file_content = self._get_expected_output("calculator", "pkg/calculator.py", MAX_CHARS)
        self.assertEqual(get_file_content("calculator", "pkg/calculator.py"), file_content)

    def test_bin_cat(self): 
        actual_output = get_file_content("calculator", "/bin/cat")
        self.assertIn('Error: Cannot read "/bin/cat" as it is outside the permitted working directory', actual_output)

    def test_file_not_existing(self):
        actual_output = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertIn('Error: File not found or is not a regular file: "pkg/does_not_exist.py"', actual_output)


if __name__ == "__main__":  
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    unittest.main()
