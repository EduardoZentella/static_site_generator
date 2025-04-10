import unittest

from utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nSome content."
        expected_title = "Title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_title(self):
        markdown = "Some content."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_invalid_type(self):
        markdown = 12345
        with self.assertRaises(TypeError):
            extract_title(markdown)