import json
import pkg_resources
import sys
import os

# Define the file to scan
file_path = r"enter_file_path_here"  # Update this with your actual file path

# Ensure the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ File not found: {file_path}")

# Extract code based on file type
code_lines = []

if file_path.endswith(".ipynb"):
    # Process Jupyter Notebook (.ipynb)
    with open(file_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    # Extract all code cells, ensuring the "source" field is processed correctly
    code_cells = [
        "\n".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        for cell in nb_data["cells"] if cell["cell_type"] == "code"
    ]

    # Flatten the code into lines
    code_lines = [line.strip() for cell in code_cells for line in cell.split("\n")]

elif file_path.endswith(".py"):
    # Process Python script (.py)
    with open(file_path, "r", encoding="utf-8") as f:
        code_lines = [line.strip() for line in f.readlines()]

else:
    raise ValueError("❌ Unsupported file type. Please provide a .ipynb or .py file.")

# Extract import statements
import_lines = [line for line in code_lines if line.startswith("import") or line.startswith("from")]

# Extract package names
packages = set()
for line in import_lines:
    parts = line.split()
    if parts[0] == "import":
        packages.add(parts[1].split(".")[0])
    elif parts[0] == "from":
        packages.add(parts[1].split(".")[0])

# Get versions of installed packages
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
requirements = [f"{pkg}=={installed_packages.get(pkg, 'latest')}" for pkg in packages]

# Determine the directory where the file is stored
file_dir = os.path.dirname(file_path)  # Get directory of the input file
requirements_path = os.path.join(file_dir, "requirements.txt")  # Save it there

# Save requirements.txt in the same folder as the input file
with open(requirements_path, "w") as f:
    f.write("\n".join(requirements))

print(f"✅ requirements.txt created successfully at: {requirements_path}")