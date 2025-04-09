from textnode import TextNode, TextType
import os
import shutil

def main():
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test)
    print("Copying files from static to public directory")
    copy_files_to_public()
    print("Files copied successfully")

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
    

        



if __name__ == "__main__":
    main()