<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD028 -->

# UtilMD

<p align="center">
  <img src=".assets/utilmd-project-banner-rev2.png" alt="UtilMD Project Banner" width="100%">
</p>

[![Static Badge](https://img.shields.io/badge/Python%203.12+-FFDE57?style=plastic&label=Requirement&link=https%3A%2F%2Fwww.python.org%2Fdownloads)](https://www.python.org/downloads)
![Static Badge](https://img.shields.io/badge/Docker-blue?style=plastic&logo=docker&logoColor=white)

UtilMD (Utility-MD) is a set of Python tools and utilities for automating tedious tasks such as creating MOC files, indexes/Table of Contents, and more.

## Installation

```bash
git clone https://github.com/NCSickels/UtilMD.git
cd UtilMD
pip install -r requirements.txt
```

## Usage

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
            v0.1.0            Noah Sickels (@NCSickels)
        =======================================================

usage: utilmd.py [options]... <input file | directory> [exclude_dirs]... [output_file]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file or directory
  -e [EXCLUDE_DIRS ...], --exclude-dirs [EXCLUDE_DIRS ...]
                        Directories to exclude.
  -o OUTPUT, --output OUTPUT
                        Output file
  -m, --moc             Generate MOC
  -n, --index           Generate index
```

### MOC Generation

Given the directory structure:

```git
.
└── Project
    ├── Note_1.md
    ├── Note_2.md
    └── Source
        └── Note_3.md
```

Where Project and Source are both directories. We can generate a MOC file with the following command:

```bash
python utilmd.py -i "Project/" --moc
```

This will generate a MOC file with the following contents:

```markdown
# Project MOC

## Index Generation

---

- [[Note 1]]
- [[Note 2]]

### Source

- [[Note 3]]
```

> [!NOTE]\
> The root directory is used as the title of the MOC file but is not included in the MOC itself.

> [!WARNING]\
> There is an known issue in the current version of UtilMD where the MOC will include the generated MOC file.

### Index / Table of Contents

Given the content of a markdown file (e.g. `Notes.md`):

```markdown
## Topic 1

## Topic 2

### Subtopic 1

### Subtopic 2

## Topic 3

### Subtopic 3

#### Subtopic 4
```

We can generate an index with the following command:

```bash
python utilmd.py -i "Notes.md" --index
```

This will generate an index with the following contents:

```markdown
# Notes

## Index

- [[Notes#Topic 1 | Topic 1]]
- [[Notes#Topic 1#Topic 2 | Topic 2]]
    - [[Notes#Topic 1#Topic 2#Subtopic 1 | Subtopic 1]]
    - [[Notes#Topic 1#Topic 2#Subtopic 2 | Subtopic 2]]
- [[Notes#Topic 1#Topic 3 | Topic 3]]
    - [[Notes#Topic 1#Topic 3#Subtopic 3 | Subtopic 3]]
      - [[Notes#Topic 1#Topic 3#Subtopic 3#Subtopic 4 | Subtopic 4]]


## Topic 1

## Topic 2

### Subtopic 1

### Subtopic 2

## Topic 3

### Subtopic 3

#### Subtopic 4
```

The index will include links to each section of the markdown file with a default indentation of 4 spaces. The generated index will be inserted at the top of the markdown file. All existing content will be shifted down but will remain unchanged.

> [!NOTE]\
> The linking format is `[[file#section | display text]]`. The `file` is the name of the file without the extension, the `section` is the name of the section in the file, and the `display text` is the text that will be displayed in the index. This is primarily suited for Obsidian-flavored markdown. More formats are planned to be supported in the future.

## Directory Structure - Tree

UtilMD also includes a tree generator that can be used to generate a tree of the directory structure. An exaple of this can be seen below (same as the MOC example):

```git
.
└── Project
    ├── File_1
    ├── File_2
    └── Source
        └── File_3
```

## Known Issues

* [ ] MOC generation includes the generated MOC file.
* [ ] Index generation does not support additional markdown formats.

## Planned Features

* [ ] Support for additional markdown formats.
