import unittest
from functions.run_python import run_python

class TestWriteFile(unittest.TestCase): 
    
    def test_calculator_usage(self):
        completed_process = run_python("calculator", "main.py")
        self.assertIn("STDOUT:", completed_process)
        self.assertIn('Usage: python main.py "<expression>"', completed_process)
        self.assertIn('Example: python main.py "3 + 5"', completed_process)

    def test_calculator_add(self):
        completed_process = run_python("calculator", "main.py", ["3 + 5"])
        self.assertIn("STDOUT:", completed_process)
        self.assertIn("3 + 5", completed_process)
        self.assertIn("=", completed_process)
        self.assertIn("8", completed_process)
    
    def test_calculator_test_suite(self):
        completed_process = run_python("calculator", "tests.py")
        self.assertIn("STDERR:", completed_process)
        self.assertIn("Ran 9 tests in 0.000s", completed_process)
        self.assertIn("OK", completed_process)
    
    def test_calculator_wrong_dir(self):
        completed_process = run_python("calculator", "../main.py")
        self.assertIn('Error: Cannot execute "../main.py" as it is outside the permitted working directory', completed_process)

    def test_calculator_nonexisting_file(self):
        completed_process = run_python("calculator", "nonexistent.py")
        self.assertIn('File "nonexistent.py" not found', completed_process)

if __name__ == "__main__":
    print(run_python("calculator", "main.py"))
    print(run_python("calculator", "main.py", ["3 + 5"]))
    print(run_python("calculator", "tests.py"))
    print(run_python("calculator", "../main.py"))
    print(run_python("calculator", "nonexistent.py"))
    unittest.main()
