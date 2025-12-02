<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD028 -->

# UtilMD

<p align="center">
  <img src=".assets/utilmd-project-banner-rev2.png" alt="UtilMD Project Banner" width="100%">
  <img alt="Python Badge" src="https://img.shields.io/badge/Python%203.12+-FFDE57?style=plastic&label=Requirement&link=https%3A%2F%2Fwww.python.org%2Fdownloads">
  <img alt="Markdown Badge" src="https://img.shields.io/badge/Markdown-000000?style=plastic&logo=markdown&logoColor=white">
  <img alt="Obsidian Badge" src="https://img.shields.io/badge/Obsidian-%23483699.svg?style=plastic&logo=obsidian&logoColor=white">
</p>

UtilMD (Utility-MD) is a set of Python tools and utilities for automating tedious tasks such as creating MOC files, indexes/Table of Contents, and more.

## Installation

```bash
# Clone the repository
git clone https://github.com/NCSickels/UtilMD.git
cd UtilMD

# (OPTIONAL) Ensure utilmd.py is executable
chmod +x utilmd.py

# (OPTIONAL) Move utilmd.py to a directory in your PATH, e.g. /usr/local/bin
sudo mv utilmd.py /usr/local/bin/utilmd
```

## Usage

> [!WARNING]\
> If you get a `python3\r: no such file or directory` error or `use -[v]S to pass options in shebang lines` message, you may need to convert the file to Unix format. This can be done with the following command: `dos2unix utilmd.py`.

```bash
python utilmd.py --help

        =======================================================
            ██╗   ██╗████████╗██╗██╗     ███╗   ███╗██████╗
            ██║   ██║╚══██╔══╝██║██║     ████╗ ████║██╔══██╗
            ██║   ██║   ██║   ██║██║     ██╔████╔██║██║  ██║
            ██║   ██║   ██║   ██║██║     ██║╚██╔╝██║██║  ██║
            ╚██████╔╝   ██║   ██║███████╗██║ ╚═╝ ██║██████╔╝
             ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝
        =======================================================
            v0.1.5            Noah Sickels (@NCSickels)
        =======================================================

usage: utilmd.py [options]... <input file | directory> [exclude_dirs]... [output_file]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file or directory
  -o OUTPUT, --output OUTPUT
                        Output file
  -m, --moc             Generate MOC
  -n, --index           Generate index
  -t, --tree            Generate directory tree.
  -e [EXCLUDE_DIRS ...], --exclude-dirs [EXCLUDE_DIRS ...]
                        Directories to exclude.
  -r, --include-root-moc
                        Include MOC files in the root directory.
  -c, --ignore-child-moc
                        Ignore MOC files in child directories.
  -v, --version         show program's version number and exit
```

### MOC Generation

Given the structure of an input directory (e.g. `Project/`):

```git
.
└── Project                    # Directory 
    ├── Class_Notes_1.md
    ├── Class_Notes_2.md
    ├── Project MOC.md         # (root MOC, will be excluded by default)
    └── Design                 # Directory
        ├── Class_Notes_3.md
        └── Design MOC.md      # (child MOC, will be included by default)
```

By default, root-level MOC files (including the one being generated) are **excluded** from the generated MOC, while child MOC files (e.g., `Design MOC.md`) are **included**. This behavior can be modified with the `-r` (or `--include-root-moc`) and the `-c` (or `--ignore-child-moc`) flags. Note that the root directory is used as the title of the generated MOC file.

Generate a MOC file with the following command:

```bash
python utilmd.py -i "Project/" --moc
```

This will generate a MOC file with the following contents:

```markdown
# Project MOC

## Index Generation

---

- [[Class_Notes_1]]
- [[Class_Notes_2]]

### Design

- [[Class_Notes_3]]
- [[Design MOC]]
```

> [!NOTE]\
> The root directory is used as the title of the generated MOC file.

### Index / Table of Contents

Given the content of a markdown file (e.g. `Notes.md`):

```markdown
## Introduction

## Networking

### TCP/IP

### Firewalls

## Cryptography

### Symmetric Encryption

#### AES
```

Generate an index with the following command:

```bash
python utilmd.py -i "Notes.md" --index
```

This will generate an index with the following contents:

```markdown
# Notes

## Index

- [[Notes#Introduction | Introduction]]
- [[Notes#Networking | Networking]]
    - [[Notes#Networking#TCP/IP | TCP/IP]]
    - [[Notes#Networking#Firewalls | Firewalls]]
- [[Notes#Cryptography | Cryptography]]
    - [[Notes#Cryptography#Symmetric Encryption | Symmetric Encryption]]
      - [[Notes#Cryptography#Symmetric Encryption#AES | AES]]


## Introduction

## Networking

### TCP/IP

### Firewalls

## Cryptography

### Symmetric Encryption

#### AES
```

The index will include links to each section of the markdown file with a default indentation of 4 spaces. The generated index will be inserted at the top of the markdown file. All existing content will be shifted down but will remain unchanged.

> [!NOTE]\
> The linking format is `[[file#section | display text]]`. In this format, `file` refers to the file name without its extension, `section` is the name of the specific section within that file, and `display text` is the text displayed in the index. This format is primarily designed for Obsidian-flavored markdown. More formats are expected to be supported in the future.

## Directory Structure - Tree

UtilMD also includes a tree generator that can be used to generate a tree of the directory structure. An example of this can be seen below (same as the MOC example):

```git
python utilmd.py -i "Project/" --tree
```

This will generate the following tree structure:

```git
.
└── Project     
    ├── Class_Notes_1.md
    ├── Class_Notes_2.md
    ├── Project MOC.md
    └── Design          
        ├── Class_Notes_3.md
        └── Design MOC.md
```

## Known Issues

* [ ] Index generation does not support additional markdown formats.

## Planned Features

* [ ] Support for additional markdown formats.
