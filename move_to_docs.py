import os
import shutil

# Files and directories to move
TO_MOVE = ["index.html", "blog", "posts"]
DOCS_DIR = "docs"

def move_to_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)
    for item in TO_MOVE:
        if os.path.exists(item):
            dest = os.path.join(DOCS_DIR, item)
            # Remove existing destination if it exists
            if os.path.exists(dest):
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                else:
                    os.remove(dest)
            # Move file or directory
            shutil.move(item, dest)
            print(f"Moved {item} to {dest}")
        else:
            print(f"Warning: {item} does not exist and was not moved.")

if __name__ == "__main__":
    move_to_docs() 