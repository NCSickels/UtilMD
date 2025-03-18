#!/usr/bin/env python3
import argparse
import json
import os
import logging

__version__ = "0.1.4"


class UtilMD:
    """
    Utility class for generating markdown files.

    Attributes:
        directory (str): The current working directory.
        exclude_dirs (list): A list of directories to exclude from any operation.
        files_and_folders (dict): A dictionary containing all files and folders in a directory.
        folder_name (str): The name of the current directory.
        output_file_name (str): The name of the output file.
        file_path (str): The path to the output file.
        new_file (str): The newly created output file.
        version (str): The current version of the script.
    """

    def __init__(self):
        self.directory = os.getcwd()
        self.exclude_dirs = [
            ".history",
            ".git",
            ".assets",
            "_images",
            "_assets",
            "test",
        ]
        self.files_and_folders = None
        self.folder_name = os.path.basename(self.directory) or ""
        self.output_file_name = ""
        self.file_path = ""
        self.new_file = None
        self.version = __version__
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def banner(self) -> None:
        print(f"""
        =======================================================
            ██╗   ██╗████████╗██╗██╗     ███╗   ███╗██████╗
            ██║   ██║╚══██╔══╝██║██║     ████╗ ████║██╔══██╗
            ██║   ██║   ██║   ██║██║     ██╔████╔██║██║  ██║
            ██║   ██║   ██║   ██║██║     ██║╚██╔╝██║██║  ██║
            ╚██████╔╝   ██║   ██║███████╗██║ ╚═╝ ██║██████╔╝
             ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝
        =======================================================
            v{self.version}            Noah Sickels (@NCSickels)
        =======================================================
             """)

    def run(self) -> None:
        parser = argparse.ArgumentParser(
            usage="%(prog)s [options]... <input file | directory> [exclude_dirs]... [output_file]"
        )
        parser.add_argument("-i", "--input", type=str, help="Input file or directory")
        parser.add_argument(
            "-e", "--exclude-dirs", nargs="*", help="Directories to exclude."
        )
        parser.add_argument("-o", "--output", type=str, help="Output file")
        parser.add_argument(
            "-m", "--moc", dest="moc", action="store_true", help="Generate MOC"
        )
        parser.add_argument(
            "-n", "--index", dest="index", action="store_true", help="Generate index"
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s v{self.version}"
        )
        parser.add_argument(
            "-t", "--tree", action="store_true", help="Generate directory tree."
        )

        args = parser.parse_args()

        self.handle_input(args)
        self.handle_output(args)
        self.handle_exclude_dirs(args)

        if args.moc:
            self.generate_moc_file()
        elif args.index and args.input:
            self.generate_index(args.input, args.output)
        elif args.tree:
            self.print_tree(self.directory, self.output_file_name)
        else:
            self.banner()
            parser.print_help()

    def handle_input(self, args) -> None:
        self.banner()
        if args.input:
            self.logger.debug(f"Input file/directory: {args.input}")
            self.directory = os.path.normpath(args.input)
            if not os.path.exists(self.directory):
                self.logger.error(f"Path does not exist: {self.directory}")
                exit(1)
            if os.path.isdir(self.directory):
                if args.index:
                    self.logger.error("Index generation requires a file input!")
                    exit(1)
                self.logger.info(f"Input directory: {self.directory}")
                self.files_and_folders = self.get_files_and_folders(
                    self.directory, self.exclude_dirs
                )
                self.folder_name = os.path.basename(self.directory)
                self.file_path = self.directory
            elif os.path.isfile(self.directory):
                self.logger.info(f"Input file: {self.directory}")
                self.file_path = self.directory
                self.directory = os.path.dirname(self.directory)
                self.folder_name = os.path.basename(self.directory)

    def handle_output(self, args) -> None:
        if args.output:
            self.output_file_name = args.output
            self.file_path = os.path.join(self.directory, self.output_file_name)

    def handle_exclude_dirs(self, args) -> None:
        if args.exclude_dirs:
            self.exclude_dirs = args.exclude_dirs

    def generate_moc_file(self) -> None:
        self.output_file_name = (
            f"{self.folder_name} MOC.md"
            if os.path.isdir(self.directory)
            else f"{os.path.splitext(os.path.basename(self.file_path))[0]} MOC.md"
        )
        self.file_path = os.path.join(self.directory, self.output_file_name)
        with open(self.file_path, "w") as self.new_file:
            self.files_and_folders = self.get_files_and_folders(
                self.directory, self.exclude_dirs
            )
            title = (
                os.path.splitext(self.folder_name)[0]
                if os.path.isdir(self.directory)
                else os.path.splitext(os.path.basename(self.file_path))[0]
            )
            self.new_file.write(f"# {title} MOC\n\n")
            self.new_file.write("## Index\n\n")
            self.new_file.write("---\n\n")
            try:
                self.generate_moc(self.files_and_folders, self.directory, True)
                self.logger.info("MOC successfully generated!")
            except Exception as e:
                self.logger.error(f"{e}")
                self.logger.error("Failed to generate MOC!")

    def generate_moc(
        self, result: dict, directory: str, header: bool = False, level: int = 3
    ) -> None:
        """
        Generate a markdown file with a table of contents (MOC) for a given directory.

        Args:
            result (dict): The result of the get_files_and_folders function.
            directory (str): The directory to generate the MOC for.
            header (bool, optional): Whether to include headers. Defaults to False.
            level (int, optional): The level of the header. Defaults to 3.

        Returns:
            None
        """
        _files = result.get("files", [])
        _subfolders = {k: v for k, v in result.items() if k != "files"}

        for file in _files:
            # Exclude the current script file
            if file != os.path.basename(__file__):
                output_file_name = os.path.splitext(file)[0].replace("_", " ")
                if self.new_file:
                    self.new_file.write(f"- [[{output_file_name}]]\n")

        if _files and self.new_file:
            self.new_file.write("\n")

        for key, value in _subfolders.items():
            if key not in self.exclude_dirs:
                if header and self.new_file:
                    self.new_file.write("#" * level + " " + key + "\n\n")
                self.generate_moc(
                    value, os.path.join(directory, key), header, level + 1
                )

    def generate_index(self, input_file: str = "", output_file: str = "") -> None:
        """
        Generate an index of all headers in a markdown file.

        Args:
            input_file (str): The input file to read.
            output_file (str): The output file to write the index to.

        Returns:
            None
        """

        headers = self.get_headers(input_file)
        existing_contents = self.get_contents(input_file)
        index_content = []
        output_file = output_file if output_file else input_file
        root_parent_header = os.path.splitext(os.path.basename(input_file))[0].replace(
            "_", " "
        )

        header_stack = []

        for header in headers:
            level = header.count("#")
            header_text = header.lstrip("#").strip()
            while len(header_stack) >= level:
                header_stack.pop()

            header_stack.append(header_text)
            full_header_path = f"{root_parent_header}#" + "#".join(header_stack)
            if level == 2:
                index_content.append(f"- [[{full_header_path} | {header_text}]]")
            else:
                tab_level = "  " * (level - 1)
                index_content.append(
                    f"{tab_level}- [[{full_header_path} | {header_text}]]"
                )

        with open(output_file, "w", newline="\n") as f:
            lines = existing_contents.split("\n")
            for line in lines:
                f.write(line + "\n")
                if line.startswith("# "):  # Level 1 heading
                    f.write("\n## Index\n\n")
                    f.write("\n".join(index_content))
                    f.write("\n\n")
        self.logger.info("Index successfully generated!")
        self.logger.info(f"Index written to: {output_file}")

    def get_files_and_folders(self, directory: str, exclude_dirs: list = []) -> dict:
        """
        Recursively get all files and folders in a directory.

        Args:
            directory (str): The directory to search.
            exclude_dirs (list, optional): List of directories to exclude. Defaults to [].

        Returns:
            dict: A dictionary containing all files and folders in the directory.
        """
        _result = {}

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if "files" not in _result:
                    _result["files"] = []
                _result["files"].append(item)
            elif os.path.isdir(item_path) and item not in exclude_dirs:
                _result[item] = self.get_files_and_folders(item_path, exclude_dirs)
        return _result

    def get_headers(self, input_file: str = "") -> list:
        """
        Get all headers from a markdown file.

        Args:
            input_file (str, optional): The input file to read. Defaults to None.

        Returns:
            _headers: A list of headers in the markdown file.
        """
        _headers = []
        input_file = input_file if input_file else self.file_path
        with open(input_file, "r") as f:
            for line in f:
                if line.startswith("#") and line.count("#") > 1:
                    _headers.append(line.strip())
        return _headers

    def get_contents(self, input_file: str = "") -> str:
        """
        Get the contents of a file.

        Args:
            input_file (str): The input file to read. Defaults to None.

        Returns:
            str: The contents of the file.
        """
        if input_file is None:
            input_file = self.file_path

        if os.path.isfile(input_file):
            try:
                with open(input_file, "r") as f:
                    return f.read()
            except Exception as e:
                print(f"Error: {e}")
                return ""
        return ""

    def dump_contents(self) -> None:
        print(json.dumps(self.files_and_folders, sort_keys=True, indent=4))

    def generate_tree(
        self, root_dir, prefix: str = "", exclude_dirs: list = []
    ) -> list:
        """
        Generates a visual representation of the directory tree structure.

        Args:
            root_dir (str): The root directory from which to generate the tree.
            prefix (str, optional): The prefix to use for each line of the tree. Defaults to empty string "".
            exclude_dirs (list, optional): List of directories to exclude from the tree. Defaults to None.

        Returns:
            tree: A list of strings, each representing a line in the directory tree.
        """
        if exclude_dirs is None:
            exclude_dirs = self.exclude_dirs

        tree = []
        contents = sorted(os.listdir(root_dir))
        pointers = [("├── ", "│   "), ("└── ", "    ")]

        for index, name in enumerate(contents):
            path = os.path.join(root_dir, name)
            if name in exclude_dirs:
                continue
            if index == len(contents) - 1:
                tree.append(prefix + pointers[1][0] + name)
                if os.path.isdir(path):
                    tree.extend(
                        self.generate_tree(path, prefix + pointers[1][1], exclude_dirs)
                    )
            else:
                tree.append(prefix + pointers[0][0] + name)
                if os.path.isdir(path):
                    tree.extend(
                        self.generate_tree(path, prefix + pointers[0][1], exclude_dirs)
                    )
        return tree

    def print_tree(self, root_dir: str, output_file: str = "") -> None:
        """
        Prints the directory tree structure starting from the given root directory.

        Args:
            root_dir (str): The root directory from which to generate the tree structure.
            output_file (str, optional): The file path where the tree structure should be written.
                                        If None, the tree structure is not written to a file.

        Returns:
            None
        """
        print(root_dir)
        tree = self.generate_tree(root_dir, exclude_dirs=self.exclude_dirs)
        if output_file:
            with open(output_file, "w") as f:
                f.write(root_dir + "\n")
                for line in tree:
                    f.write(line + "\n")
        for line in tree:
            print(line)


def main() -> None:
    markdown_utilities = UtilMD()
    markdown_utilities.run()


if __name__ == "__main__":
    main()
