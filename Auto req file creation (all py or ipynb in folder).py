import json
import pkg_resources
import sys
import os

# Define the folder to scan (directory containing .py and .ipynb files)
folder_path = r"enter_folder_path_here"  # Update this with your actual folder path

# Ensure the folder exists
if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
    raise NotADirectoryError(f"❌ Directory not found: {folder_path}")

# Initialize a list for storing all code lines from all files
code_lines = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Process only Jupyter Notebook (.ipynb) and Python (.py) files
    if filename.endswith(".ipynb"):
        with open(file_path, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
        # Extract all code cells from the notebook
        code_cells = [
            "\n".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
            for cell in nb_data.get("cells", []) if cell.get("cell_type") == "code"
        ]
        # Split each code cell into lines and add to our list
        for cell in code_cells:
            code_lines.extend([line.strip() for line in cell.split("\n")])
    elif filename.endswith(".py"):
        with open(file_path, "r", encoding="utf-8") as f:
            file_lines = f.readlines()
            code_lines.extend([line.strip() for line in file_lines])

if not code_lines:
    print("No Python (.py) or Jupyter Notebook (.ipynb) files found in the directory.")
    sys.exit(0)

# Extract import statements from the collected code lines
import_lines = [line for line in code_lines if line.startswith("import") or line.startswith("from")]

# Extract package names from the import statements
packages = set()
for line in import_lines:
    parts = line.split()
    if not parts:
        continue
    if parts[0] == "import":
        # Handle multiple imports in one line (e.g., "import os, sys")
        imports = line[len("import"):].split(",")
        for imp in imports:
            pkg = imp.strip().split()[0]  # ignore aliasing if present
            packages.add(pkg.split(".")[0])
    elif parts[0] == "from":
        if len(parts) >= 2:
            pkg = parts[1].split('.')[0]
            packages.add(pkg)

# Get versions of installed packages
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
requirements = []
for pkg in packages:
    # Convert package name to lowercase for matching installed packages keys
    version = installed_packages.get(pkg.lower(), 'latest')
    requirements.append(f"{pkg}=={version}")

# Save requirements.txt in the same folder
requirements_path = os.path.join(folder_path, "requirements.txt")
with open(requirements_path, "w", encoding="utf-8") as f:
    f.write("\n".join(requirements))

print(f"✅ requirements.txt created successfully at: {requirements_path}")
