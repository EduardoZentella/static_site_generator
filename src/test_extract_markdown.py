import unittest

from utils import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_image_single(self):
        text = "![alt text](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/image.png")]
        )

    def test_image_multiple(self):
        text = "![a](img1.png) y ![b](img2.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a", "img1.png"), ("b", "img2.png")]
        )

    def test_image_empty_alt(self):
        text = "![](http://example.com/blank.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "http://example.com/blank.png")]
        )

    def test_image_no_match(self):
        text = "Esto es texto con [un link](url.com)."
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_special_chars(self):
        text = "![imagen $%&](image_%20special.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("imagen $%&", "image_%20special.jpg")]
        )

    def test_image_nested_brackets(self):
        text = "![alt con [corchetes]](image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt con [corchetes]", "image.png")]
        )

    def test_image_mixed_content(self):
        text = "Texto ![img](img.png) y [link](url.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img", "img.png")]
        )

    def test_image_invalid_syntax(self):
        text = "![alt faltan paréntesis (url"
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_empty_input(self):
        self.assertEqual(extract_markdown_images(""), [])

class TestMarkdownLinks(unittest.TestCase):
    def test_link_single(self):
        text = "[link text](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link text", "https://example.com")]
        )

    def test_link_multiple(self):
        text = "[a](url1) y [b](url2)"
        self.assertEqual(
            extract_markdown_links(text),
            [("a", "url1"), ("b", "url2")]
        )

    def test_link_empty_text(self):
        text = "[](http://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "http://example.com")]
        )

    def test_link_no_match(self):
        text = "Texto con ![imagen](img.png)."
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_special_chars(self):
        text = "[texto $%&](url_%20especial)"
        self.assertEqual(
            extract_markdown_links(text),
            [("texto $%&", "url_%20especial")]
        )

    def test_link_nested_brackets(self):
        text = "[texto [anidado]](url)"
        self.assertEqual(
            extract_markdown_links(text),
            [("texto [anidado]", "url")]
        )

    def test_link_mixed_content(self):
        text = "Texto [link](url) y ![img](img.png)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "url")]
        )

    def test_link_invalid_syntax(self):
        text = "[link sin cierre(url"
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_empty_input(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_image_and_link_together(self):
        text = "![img](img.png) [link](url.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img", "img.png")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "url.com")]
        )