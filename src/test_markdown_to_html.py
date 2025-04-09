import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_heading(self):
        md = """
            # This is a heading

            ## This is a subheading

            ### This is a sub-subheading

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a subheading</h2><h3>This is a sub-subheading</h3></div>",
        )
    
    def test_quote(self):
        md = """
            > This is a quote
            > that spans multiple lines
            > and has **bold** text

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans multiple lines and has <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
            - Item 1
            - Item 2
            - Item 3

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
            1. Item 1
            2. Item 2
            3. Item 3

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )
    
    def test_paragraph_image(self):
        md = """
            ![alt text](https://example.com/image.png)

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><img src=\"https://example.com/image.png\" alt=\"alt text\"></img></p></div>",
        )
    
    def test_paragraph_link(self):
        md = """
            [link text](https://example.com)

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><a href=\"https://example.com\">link text</a></p></div>",
        )
        
    