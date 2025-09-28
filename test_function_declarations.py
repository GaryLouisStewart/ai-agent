import unittest
from types import SimpleNamespace

# configure mock structures mocking the api structure

def make_function_call_part(name, args):
    return SimpleNamespace(function_call=SimpleNamespace(name=name, args=args))


def make_text_part(text):
    return SimpleNamespace(text=text)

def make_response_with_calls(calls):
    parts = [make_function_call_part(name, args) for name, args in calls]
    candidate = SimpleNamespace(content=SimpleNamespace(parts=parts))
    usage = SimpleNamespace(prompt_token_count=1, candiates_token_count=1)
    return SimpleNamespace(candidates=[candidate], usage_metadata=usage)

def make_response_with_text(text):
    parts = [make_text_part(text)]
    candidate = SimpleNamespace(content=SimpleNamespace(parts=parts))
    usage = SimpleNamespace(prompt_token_count=1, candidates_token_count=1)
    return SimpleNamespace(candidates=[candidate], usage_metadata=usage)


class MockClient:
    def __init__(self, response):
        self._response = response
        self.models = SimpleNamespace(generate_content=self._generate)

    def _generate(self, model, contents, config):
        return self._response

def capture_stdout(fn, *args, **kwargs):
    from io import StringIO
    import sys
    old = sys.stdout
    try:
        buf = StringIO()
        sys.stdout = buf
        fn(*args, **kwargs)
        return buf.getvalue()
    finally:
        sys.stdout = old

import main as app


class TestGenerateContent(unittest.TestCase):
    def test_prints_function_call_for_root(self):
        response = make_response_with_calls([("get_files_info", {"directory": "."})])
        client = MockClient(response)

        out = capture_stdout(app.generate_content, client, [], verbose=False)
        self.assertIn("Calling function: get_files_info({'directory': '.'})", out)


    def test_prints_function_call_for_pkg(self):
        response = make_response_with_calls([("get_files_info", {"directory": "pkg"})])
        client = MockClient(response)

        out = capture_stdout(app.generate_content, client, [], verbose=False)
        self.assertIn("Calling function: get_files_info({'directory': 'pkg'})", out)


    def text_falls_back_to_text_when_no_calls(self):
        response = make_response_with_text("Hello world")
        client = MockClient(response)

        out = capture_stdout(app.generate_content, client, [], verbose=False)
        self.assertIn("Hello world", out)
        self.assertNotIn("Calling function:", out)

    def test_multiple_calls_printed(self):
        response = make_response_with_calls([
            ("get_files_info", {"directory": "."}),
            ("get_files_info", {"directory": "pkg"}),
        ])
        client = MockClient(response)

        out = capture_stdout(app.generate_content, client, [], verbose=False)
        self.assertIn("get_files_info({'directory': '.'})", out)
        self.assertIn("get_files_info({'directory': 'pkg'})", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
