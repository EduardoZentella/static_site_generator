from textnode import TextNode, TextType
from markdown_to_html import markdown_to_html_node
import os
import sys
import shutil

def main():
    basepath = sys.argv[0] if sys.argv[0] else "/"
    copy_files_to_docs()
    print("Generating pages from markdown files")
    generate_pages_recursively("content", "template.html", "docs", basepath)
    

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

def copy_files_to_docs():
    """
    Copies all files from static to the docs directory.
    """
    static_dir = "static"
    public_dir = "docs"
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    updated_page = page_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    with open(dest_path, 'w') as f:
        f.write(updated_page)
    print(f"Page generated at {dest_path}")

def generate_pages_recursively(dir_path_content, template_path, dest_path_content, basepath):
    """
    Generates pages recursively from a directory of markdown files.
    """
    if not os.path.exists(dest_path_content):
        os.makedirs(dest_path_content)
    
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_path_content, item)
        
        if os.path.isdir(src_path):
            generate_pages_recursively(src_path, template_path, dest_path, basepath)
        elif src_path.endswith(".md"):
            dest_file_name = f"{os.path.splitext(item)[0]}.html"
            dest_file_path = os.path.join(dest_path_content, dest_file_name)
            generate_page(src_path, template_path, dest_file_path, basepath)

if __name__ == "__main__":
    main()