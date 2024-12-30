<!-- markdownlint-disable MD033 -->
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
