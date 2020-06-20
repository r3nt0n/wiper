![[Version 0.5~beta](https://github.com/R3nt0n)](http://img.shields.io/badge/version-v0.5~beta-orange.svg)
![[Python 3.2+](https://github.com/R3nt0n)](http://img.shields.io/badge/python-3.2+-blue.svg)
![[GPL-3.0 License](https://github.com/R3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)

<p align="center"><img src="https://github.com/R3nt0n/wiper/blob/master/img/wiper-0.5.gif" /></p>

# wiper
Toolkit to perform secure destruction of sensitive virtual data, temporary files and swap memories.

It has been **designed to make tasks about personal data destruction easier**, those which remain on work computers **when employees leave the company**.

## Features
+ **MANUAL wipe selection**. You can wipe single files, whole directories and free space in partitions.
+ **AUTO wipe selection**. Suggests an automatic selection of paths to wipe, relatives to personal/temporary data and swap memories.  
**If you run it with the OS target unmounted**, e.g. from a live OS trying to wipe an 
unmounted hard drive containing another OS, you should provide the root path/mount point to that system in order to use auto-search mode.

## How it works
+ You can **wipe single/multiple files** and **wipe free space** by manual selection.
+ Auto-search mode is able to **scan and suggest sensitive paths that are tipically candidates to wipe**.
+ It **overwrites existing data or free space** with one-pass pseudo-random bytes.
+ **Paths** provided **can be absolute or relative**, but **don't allow wildcards**.

## Requirements
+ Python 3
+ wmi (if you want to use auto-search mode booted on a Windows OS)

## Usage
```

  -h, --help            show this help message and exit
  -i, --interactive     interactive mode, the script will guide you
  -w, --free-space      wipe all free space on given path
  -p path, --path path  path to partition/file you want to wipe (required in non-interactive mode)


``` 

## Changelist
##### 0.5~beta version notes (20/06/2020)
+ Manual options (wipe free space and wipe single/multiple files) implemented.


## TODO list
+ Add **other one-pass overwriting methods** to:
    + choose between them in a **single-pass mode**
    + combine them in a **multi-pass mode**


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.