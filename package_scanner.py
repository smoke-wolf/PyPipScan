import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QWidget, QVBoxLayout, \
    QLabel, QTextEdit, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Package Scanner")
        self.resize(400, 300)

        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create the "Clear pycache" button
        clear_button = QPushButton("Clear pycache")
        clear_button.clicked.connect(self.clear_pycache)
        layout.addWidget(clear_button)

        # Create the directory selection label and button
        label = QLabel("Select a directory:")
        layout.addWidget(label)

        button = QPushButton("Browse")
        button.clicked.connect(self.browse_directory)
        layout.addWidget(button)

        # Create the text area to display package information
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Create the "Generate Packages" button
        generate_button = QPushButton("Generate Packages")
        generate_button.clicked.connect(self.generate_packages)
        layout.addWidget(generate_button)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")

        if dir_path:
            self.directory_path = dir_path

    
    def remove_pycache(directory):
        for root, dirs, files in os.walk(directory):
            # Remove __pycache__ directories
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    dir_path = os.path.join(root, dir_name)
                    print(f"Removing directory: {dir_path}")
                    shutil.rmtree(dir_path)
    
            # Remove .pyc files
            for file_name in files:
                if file_name.endswith(".pyc"):
                    file_path = os.path.join(root, file_name)
                    print(f"Removing file: {file_path}")
                    os.remove(file_path)

    def generate_packages(self):
        try:
            # Check if a directory is selected
            if not hasattr(self, "directory_path"):
                raise ValueError("No directory selected")

            # Scan the directory for packages
            packages = self.scan_directory(self.directory_path)

            # Write the packages to the text area
            self.text_edit.clear()
            if packages:
                self.text_edit.append("Packages Used:")
                for package in packages:
                    self.text_edit.append(package)
            else:
                self.text_edit.append("No packages found.")

            # Show a message box to the user
            QMessageBox.information(self, "Success", "Packages compiled successfully!")

        except Exception as e:
            # Show an error message box
            QMessageBox.critical(self, "Error", f"Error: {e}")

    def extract_package_name(self, line):
        # Remove leading/trailing whitespaces and split the line
        parts = line.strip().split()

        # Extract the package name from the line
        if parts:
            if parts[0] == "import":
                package_name = parts[1]
            elif parts[0] == "from" and parts[2] == "import":
                package_name = parts[1]
            else:
                package_name = None
            if package_name:
                package_name = package_name.split(".")[0]  # Extract only the first part of package name
            return package_name

        return None

    def scan_directory(self, directory):
        packages = set()

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith("import") or line.startswith("from"):
                                package_name = self.extract_package_name(line)
                                if package_name:
                                    packages.add(package_name)

        return packages


if __name__ == "__main__":
    import sys

    # Create the PyQt5 application
    app = QApplication(sys.argv)

    # Set the application style
    app.setStyle("Fusion")

    # Set a custom stylesheet for a modern look
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: black;
        }
        QLabel {
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 8px;
        }
        QTextEdit {
            background-color: black;
            border: 1px solid #d0d0d0;
            padding: 5px;
            font-family: Courier, monospace;
        }
        QPushButton {
            background-color: #4c8dff;
            color: gold;
            font-size: 14px;
            padding: 8px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #2d70ff;
        }
        QPushButton:pressed {
            background-color: #1c47b3;
        }
        """
    )

    # Create the main window and show it
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
