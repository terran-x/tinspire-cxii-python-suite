# Script to build a .tns file from Python files in a specified directory using the Luna compiler.
import sys
import os
import subprocess
from pathlib import Path

# Collect python files in target directory and build a .tns file
def buildTNSFile(path,entry_file='main.py'):
    py_files = fetchPyFiles(path)
    entry_filepath = os.path.join(path, entry_file)
    root_path = Path(__file__).resolve().parent

    if entry_filepath in py_files:
        py_files = entryToFront(py_files, entry_filepath)
    
    if not py_files:
        raise FileNotFoundError(f"No Python files found in: {path}")
    
    # Create a .tns file with the collected python files
    tns_file_path = os.path.join(path, os.path.basename(os.path.normpath(path)) + '.tns')

    # Clean up any existing .tns file before building a new one
    if os.path.exists(tns_file_path):
        os.remove(tns_file_path)
    
    luna_command = ["wsl", "luna"] + [linuxStylePath(stripRootPath(f, root_path)) for f in py_files] + [linuxStylePath(stripRootPath(tns_file_path, root_path))]

    try:
        subprocess.run(luna_command, check=True, cwd=root_path)
        print(f"Built {tns_file_path} with the following Python files:")
        for py_file in py_files:
            print(f"- {py_file}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Luna failed to compile {tns_file_path}: {e}")

# Format file paths to linux style for compatibility with the Luna compiler
def linuxStylePath(path):
    return path.replace("\\", "/")

# Strip the root path from the file path for character limit safety
def stripRootPath(path, root_path):
    return os.path.relpath(path, root_path)

# Move entry point python file to front of the list
def entryToFront(py_files, entry_file):
    if entry_file in py_files:
        py_files.remove(entry_file)
        py_files.insert(0, entry_file)
    return py_files

# Function to fetch all Python files in the target directory
def fetchPyFiles(path):
    py_files = []
    for file in os.listdir(path):
        if file.endswith('.py'):
            py_files.append(os.path.join(path, file))
    return py_files

def buildAllProjects():
    root_path=Path(__file__).resolve().parent
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Guard against hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        # Guard against the root directory itself
        if Path(dirpath) == root_path:
            continue
        has_python_files = any(f.endswith('.py') for f in filenames)
        if has_python_files:
            try:
                buildTNSFile(dirpath)
            except Exception as e:
                print(f"Error building project in {dirpath}: {e}")

# Check if the script is run directly and handle command-line arguments
if __name__ == "__main__":
    # Check if the user is asking for help or instructions
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Automates the compilation of multiple .py files into a single multi-page .tns file.

Install Luna compiler and ensure it's in your system's PATH.

Usage:
  python build.py                      -> Scans for and auto-compiles every project folder.
  python build.py [path]               -> Compiles a specific project folder using 'main.py' 
                                          as the primary entry page.
  python build.py [path] [entry_file]  -> Compiles a specific project folder using your 
                                          custom filename as the primary entry page.

        """)
        sys.exit(0)
    if len(sys.argv) > 1:
        build_args = {"path": sys.argv[1]}

        if sys.argv[2:]:
            build_args["entry_file"] = sys.argv[2]

        buildTNSFile(**build_args)
    else:
        buildAllProjects()