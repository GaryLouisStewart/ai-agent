import call_function as cf
from google.genai import types
import unittest
from unittest import mock
from io import StringIO
import sys


class FakeFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        

class TestCallFunction(unittest.TestCase):
    def test_valid_file_content(self):
        fc = FakeFunctionCall(
            name="get_file_content",
            args={"file_path": "lorem.txt"},
        )
        result = cf.call_function(fc, verbose=False)

        self.assertIsInstance(result, types.Content)
        self.assertEqual(result.role, "tool")
        self.assertTrue(result.parts)
        fr = result.parts[0].function_response
        self.assertIsNotNone(fr)
        self.assertEqual(fr.name, "get_file_content")
        self.assertIsInstance(fr.response, dict)
        self.assertIn("result", fr.response)
        self.assertIsInstance(fr.response["result"], str)
        self.assertTrue(len(fr.response["result"]) > 0)


    def test_unknown_function(self):
        fc = FakeFunctionCall(name="not_a_function", args={})
        result = cf.call_function(fc, verbose=False)
        fr = result.parts[0].function_response
        self.assertIn("error", fr.response)

    @mock.patch("call_function.FUNCTIONS_MAP", {"get_files_info": mock.Mock(return_value="ok")})
    def test_injects_working_directory(self):
        fc = FakeFunctionCall("get_files_info", {})
        result = cf.call_function(fc, verbose=False)
        func_mock = cf.FUNCTIONS_MAP["get_files_info"]
        func_mock.assert_called_once()
        kwargs = func_mock.call_args.kwargs
        self.assertEqual(kwargs.get("working_directory"), "./calculator")
        self.assertIsNotNone(result.parts[0].function_response)


    def test_verbose_prints_call_line(self):
        fc = FakeFunctionCall("get_file_content", {"file_path": "lorem.txt"})
        buf = StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            cf.call_function(fc, verbose=True)
        finally:
            sys.stdout = old
        out = buf.getvalue()
        self.assertIn("Calling function: get_file_content", out)

if __name__ == "__main__":
    unittest.main()
