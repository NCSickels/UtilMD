import os
import json
import argparse


class UtilMD:
    def __init__(self):
        self.directory = os.getcwd()
        self.exclude_dirs = ['.history', '_images', '_assets', 'test']
        self.files_and_folders = None
        self.folder_name = os.path.basename(self.directory)
        self.output_file_name = ''  # f'{self.folder_name}.md'
        self.file_path = None
        # os.path.join(self.directory, self.output_file_name)
        self.new_file = None
        self.version = '0.1.0'

    def banner(self):
        print(f'''
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
             ''')

    def run(self):
        parser = argparse.ArgumentParser(
            usage="%(prog)s [options]... <input file | directory> [exclude_dirs]... [output_file]")
        parser.add_argument("-i", "--input", type=str,
                            help="Input file or directory")
        parser.add_argument("-e", "--exclude-dirs", nargs="*",
                            help="Directories to exclude.")
        parser.add_argument("-o", "--output", type=str, help="Output file")
        parser.add_argument("-m", "--moc", dest="moc",
                            action="store_true", help="Generate MOC")
        parser.add_argument("-n", "--index", dest="index",
                            action="store_true", help="Generate index")
        args = parser.parse_args()

        if args.input:
            print("Input file or directory:", args.input)
            if os.path.isdir(args.input):
                print(f'Input directory: {args.input}')
                self.directory = args.input
                self.files_and_folders = self.get_files_and_folders(
                    self.directory, self.exclude_dirs)
                self.folder_name = os.path.basename(self.directory)
                self.file_path = args.input
                # os.path.join(self.directory, self.output_file_name)
            elif os.path.isfile(args.input):
                print(f'Input file: {args.input}')
                self.file_path = os.path.join(
                    self.directory, self.output_file_name)

        if args.output:
            self.output_file_name = args.output
            self.file_path = os.path.join(
                self.directory, self.output_file_name)

        if args.exclude_dirs:
            self.exclude_dirs = args.exclude_dirs

        if args.moc:
            self.output_file_name = f'{os.path.basename(self.file_path)} MOC.md' if os.path.isfile(
                self.file_path) else f'{self.folder_name} MOC.md'
            self.new_file = open(self.file_path, 'w') if not os.path.isdir(self.directory) else open(
                f'{self.directory}/{self.output_file_name}', 'w')

            self.files_and_folders = self.get_files_and_folders(
                self.directory, self.exclude_dirs)

            self.new_file.write(f'# {self.folder_name} MOC\n\n')
            self.new_file.write('## Index\n\n')
            self.new_file.write('---\n\n')
            try:
                self.generate_moc(self.files_and_folders, self.directory, True)
                print('MOC generated successfully!')
            except Exception as e:
                print(f'Error: {e}')
                print('Failed to generate MOC!')
        elif args.index and args.input and os.path.isfile(args.input):
            self.generate_index(args.input, args.output)
        else:
            self.banner()
            parser.print_help()

    def generate_moc(self, result: dict, directory: str, header=False, level=3) -> None:
        _files = result.get('files', [])
        _subfolders = {k: v for k, v in result.items() if k != 'files'}

        for file in _files:
            # Exclude the current script file
            if file != os.path.basename(__file__):
                output_file_name = os.path.splitext(file)[0].replace('_', ' ')
                self.new_file.write(f'- [[{output_file_name}]]\n')

        if _files:
            self.new_file.write('\n')

        for key, value in _subfolders.items():
            if key not in self.exclude_dirs:
                if header:
                    self.new_file.write('#' * level + ' ' + key + '\n\n')
                self.generate_moc(value, os.path.join(
                    directory, key), header, level + 1)

    def generate_index(self, input_file, output_file) -> None:
        headers = self.get_headers(input_file)
        existing_contents = self.get_contents(input_file)
        index_content = []
        output_file = output_file if output_file else input_file
        root_parent_header = os.path.splitext(os.path.basename(input_file))[
            0].replace('_', ' ')

        header_stack = []

        for header in headers:
            level = header.count('#')
            header_text = header.lstrip('#').strip()
            # index_content.append(
            #     f'{"    " * (level - 1)}- [[{root_parent_header}#{header_text} | {header_text}]]')
            while len(header_stack) >= level:
                header_stack.pop()

            header_stack.append(header_text)
            full_header_path = f'{root_parent_header}#' + \
                '#'.join(header_stack)
            if level == 2:
                index_content.append(
                    f'- [[{full_header_path} | {header_text}]]')
            else:
                tab_level = "  " * (level - 1)
                index_content.append(
                    f'{tab_level}- [[{full_header_path} | {header_text}]]')

        with open(output_file, 'w', newline='\n') as f:
            lines = existing_contents.split('\n')
            for line in lines:
                f.write(line + '\n')
                if line.startswith('# '):  # Level 1 heading
                    f.write('\n## Index\n\n')
                    f.write('\n'.join(index_content))
                    f.write('\n\n')

    def get_files_and_folders(self, directory: str, exclude_dirs=[]) -> dict:
        _result = {}

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if 'files' not in _result:
                    _result['files'] = []
                _result['files'].append(item)
            elif os.path.isdir(item_path) and item not in exclude_dirs:
                _result[item] = self.get_files_and_folders(
                    item_path, exclude_dirs)
        return _result

    def get_headers(self, input_file=None) -> list:
        _headers = []
        input_file = input_file if input_file else self.file_path
        with open(input_file, 'r') as f:
            for line in f:
                if line.startswith('#') and line.count('#') > 1:
                    _headers.append(line.strip())
        return _headers

    def get_contents(self, input_file=None) -> str:
        if os.path.isfile(input_file):
            with open(input_file, 'r') as f:
                return f.read()

    def dump_contents(self) -> None:
        print(json.dumps(self.files_and_folders, sort_keys=True, indent=4))


def main():
    markdown_utilities = UtilMD()
    markdown_utilities.run()


if __name__ == '__main__':
    main()
