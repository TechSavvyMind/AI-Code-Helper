"""Custom tools for interacting with the file system."""
import os
import logging

class FileSystemTools:
    """A collection of tools to read, write, and list files."""

    @staticmethod
    def list_files(path="."):
        """
        Lists all files and directories in a given path recursively.

        Args:
            path (str): The path to list. Defaults to the current directory.

        Returns:
            str: A string representation of the directory tree.
        """
        if not os.path.exists(path) or not os.path.isdir(path):
            return f"Error: Path '{path}' does not exist or is not a directory."

        tree = []
        try:
            for root, dirs, files in os.walk(path):
                level = root.replace(path, '').count(os.sep)
                indent = ' ' * 4 * (level)
                tree.append(f'{indent}{os.path.basename(root)}/')
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    tree.append(f'{sub_indent}{f}')
        except Exception as e:
            logging.error(f"Error listing files at path '{path}': {e}")
            return f"Error listing files: {e}"
        return "\n".join(tree)

    @staticmethod
    def read_file(file_path):
        """
        Reads the content of a specified file.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            str: The content of the file, or an error message if it fails.
        """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return f"Error: File '{file_path}' does not exist or is not a file."
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logging.info(f"Successfully read file: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Error reading file '{file_path}': {e}")
            return f"Error reading file: {e}"

    @staticmethod
    def write_file(file_path, content):
        """
        Writes content to a specified file. Overwrites the file if it exists.

        Args:
            file_path (str): The path to the file to write to.
            content (str): The content to write to the file.

        Returns:
            str: A success message, or an error message if it fails.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Successfully wrote changes to file: {file_path}")
            return f"Successfully wrote changes to {file_path}"
        except Exception as e:
            logging.error(f"Error writing to file '{file_path}': {e}")
            return f"Error writing to file: {e}"

