# Package Scanner

Package Scanner is a Python tool that allows you to scan a directory, look through it, and compile a list of all packages used in Python files. It can generate a `requirements.txt` file with the list of packages that can be installed from pip, as well as other packages found.

## Features

- Scan a directory for Python files and extract package information.
- Generate a `requirements.txt` file with the list of packages.
- Supports both `import` and `from ... import` statements.
- Provides a user-friendly GUI interface for easy interaction.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/smoke-wolf/package-scanner.git
Install the required dependencies:

## Usage
Run the package_scanner.py script:

  **python package_scanner.py**

Select a directory by clicking on the "Browse" button.

Click on the "Generate Packages" button to scan the directory and generate the requirements.txt file.

The list of packages used will be displayed in the text area. If any packages are found, they will also be saved in the requirements.txt file.
