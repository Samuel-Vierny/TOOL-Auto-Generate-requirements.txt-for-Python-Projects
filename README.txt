# Auto-Generate `requirements.txt` for Python Projects

## Overview
This script automatically scans a given **Jupyter Notebook (`.ipynb`)** or **Python script (`.py`)**, extracts its dependencies, and generates a `requirements.txt` file with the installed package versions.

## Features
- Supports both **Jupyter Notebooks** and **Python scripts**.
- Extracts `import` and `from ... import` statements.
- Identifies installed package versions to ensure correct dependencies.
- Saves the `requirements.txt` file in the **same directory** as the input file.
- Works with any Python project, making dependency management easier.

## Installation
Ensure you have Python installed on your system. This script does not require additional dependencies beyond `pkg_resources`, which is included with `setuptools`.

## Usage
### 1️⃣ **Modify the Script**
Update the `file_path` variable with the path to your **`.ipynb`** or **`.py`** file:
```python
file_path = r"/path/to/your/file.ipynb"  # or "/path/to/your/file.py"
```

### 2️⃣ **Run the Script**
Execute the script using Python:
```bash
python generate_requirements.py
```

### 3️⃣ **Find `requirements.txt`**
Once executed, the script will create a `requirements.txt` file **in the same directory** as the provided file.

### 4️⃣ **Install Dependencies**
You (or your team) can now install the required dependencies using:
```bash
pip install -r /path/to/your/requirements.txt
```

Now, `requirements.txt` will always stay up to date! 🚀

## License
This script is open-source and can be modified and shared freely.

## Contact
For any issues or suggestions, feel free to open an issue on the GitHub repository - Samuel Vierny

