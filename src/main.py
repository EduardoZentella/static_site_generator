from textnode import TextNode, TextType
from markdown_to_html import markdown_to_html_node
import os
import shutil

def main():
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test)
    print("Copying files from static to public directory")
    copy_files_to_public()
    print("Files copied successfully")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )
    

def copy_folder_contents(src, dest):
        """
        Copies all files from src to dest.
        """
        print(f"Copying files from {src} to {dest}")
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)
            print(f"Copying {src_path} to {dest_path}")
            if os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                copy_folder_contents(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)

def copy_files_to_public():
    """
    Copies all files from static to the public directory.
    """
    static_dir = "static"
    public_dir = "public"
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    # Remove existing files in public directory recursively
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    # Copy files from static to public directory with recursive copy and logging
    copy_folder_contents(static_dir, public_dir)
    print(f"Copied files from {static_dir} to {public_dir}")
    
def extract_title(markdown):
    """
    Extracts the title from a markdown string.
    """
    if not isinstance(markdown, str):
        raise TypeError("Markdown must be a string")
    
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    """
    Generates a page from a markdown file using a template.
    """
    if not isinstance(from_path, str) or not isinstance(template_path, str) or not isinstance(dest_path, str):
        raise TypeError("Paths must be strings")
    
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    with open(dest_path, 'w') as f:
        f.write(page_content)
    print(f"Page generated at {dest_path}")

if __name__ == "__main__":
    main()