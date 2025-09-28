import unittest
import os
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file_content



class testWriteFileContent(unittest.TestCase):

    def test_single_file(self):
        write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        file_content = get_file_content("calculator", "lorem.txt")
        self.assertIn("wait, this isn't lorem ipsum", file_content)

    def test_file_and_new_dir(self):
        write_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        file_content = get_file_content("calculator", "pkg/morelorem.txt")
        self.assertIn("lorem ipsum dolor sit amet", file_content)

    def test_path_outside_permitted_dir(self):
        message = write_file_content("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.assertIn('Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory', message)
        


if __name__ == "__main__":
    print(write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file_content("calculator", "/tmp/temp.txt", "this should not be allowed"))
    unittest.main()
