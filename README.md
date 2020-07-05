![[Version 1.0](https://github.com/R3nt0n)](http://img.shields.io/badge/version-v1.0-orange.svg)
![[Python 3.2+](https://github.com/R3nt0n)](http://img.shields.io/badge/python-3.2+-blue.svg)
![[GPL-3.0 License](https://github.com/R3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)

# wiper
Toolkit to perform **secure destruction of sensitive virtual data, temporary files and swap memories**.

It has been **designed to make tasks about personal data destruction easier**, for example those which remain on work computers **when employees leave the company**. Making  the entire process easier through the interactive mode and allowing it to be automated through the CLI mode, it can be useful for both the employee and the companies when cleaning personal data on PCs that is going to be reused.

You can configure your own overwrite method, choosing and combining between **ones, zeros and/or random data methods** as many times as you want (e.g.: or, rzzrozr, roozr...). By default, it performs a single one-pass with random data.


## Usage
```
usage: wiper.py [-h] [-i] [-f path] [-p path] [-r path] [-t] [-u] [-T] [-U] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     interactive mode, the script will guide you
  -f path, --free path  wipe all free space on given path
  -p path, --path path  path to dir/file you want to wipe
  -m ozr, --method ozr  overwrite methods to apply (o: ones, z: zeros, r: random),
                        you can combine it and choose the order
  -r path, --root path  set a custom root path if you want to wipe with auto-search modes
                        an unbooted system (e.g. /media/drive)
  -u, --home            auto-search mode: locate actual user home directory and wipes it
  -U, --home-all        auto-search mode: locate all users home directory and wipes it
  -s, --swaps           auto-search mode: locate swap partitions/pagefiles and wipes it
                        (be careful: UUID swap partitions also will be wiped)

``` 

### Interactive example

<p align="center"><img src="https://github.com/R3nt0n/wiper/blob/master/img/wiper-1.0-interactive.gif" /></p>

### CLI example

<p align="center"><img src="https://github.com/R3nt0n/wiper/blob/master/img/wiper-1.0-cli.gif" /></p>

### Advanced examples
+ Wipes all free space in a given partition:    
`wiper.py -f /home`  
+ Wipes all files inside a given path using zeros, ones, zeros, zeros and random methods:  
`wiper.py -p /home/user/Documents -m zozzr`  
+ Locate and wipe pagination files inside an unbooted OS (mounted on `/home/media/`) using only zeros method:    
`wiper.py -r /home/media -s -m z`  

## Features
+ You can **configure your own overwrite method**, choosing and combining between **ones, zeros and/or random data methods** as many times as you want (e.g.: or, rzzrozr, roozr...). By default, it performs a single one-pass with random data.
+ **MANUAL wipe selection**. You can wipe single files, whole directories and free space in partitions.
+ **AUTO wipe selection**. Suggests an automatic selection of paths to wipe, relatives to personal/temporary data and swap memories.  
**If you run it with the OS target unmounted**, e.g. from a live OS trying to wipe an 
unmounted hard drive containing another OS, you should provide the root path/mount point to that system in order to use auto-search mode.

## How it works
+ **This is not a backup tool**: the data will be unrecoverable, so **be sure to backup all the files you want to keep before wipe it**.
+ You can **wipe single/multiple files** and **wipe free space** by manual selection.
+ Auto-search mode is able to **scan and suggest sensitive paths that are tipically candidates to wipe**.
+ It **overwrites existing data or free space** with one-pass **pseudo-random/ones/zeros** bytes and also combine them.
+ **Paths** provided **can be absolute or relative**, but **don't allow wildcards**.
+ Be careful **when you overwrite whole partitions** (like wipe swaps feature), the **device block** (info like partitions UUID) **will be destroyed**.

## Requirements
+ Python 3
+ wmi (if you want to use auto-search mode booted on a Windows OS)

## Changelist
##### 1.0 version notes (05/07/2020)
+ Logic to choose, combine and apply diferent methods implemented.
+ Temp and temp-all features removed because it doesn't seem useful.
##### 0.9~beta version notes (29/06/2020)
+ One-pass overwrite methods already implemented: random, ones and zeros. 
+ Fixing menu bug and updating usage.
+ Added auto-search personal dirs platform independent. Added arguments for all interactive options (everything can be run from CLI or inside interactive mode)
##### 0.6~beta version notes (20/06/2020)
+ Added swap/pagefiles auto-detection system independent and random wipes feature (opt 7)
+ Manual options (wipe free space and wipe single/multiple files) implemented.
##### 0.5~beta version notes (20/06/2020)
+ Added setup.py. Converted all input paths into platform independent paths (pathlib).
+ Manual options (wipe free space and wipe single/multiple files) implemented.


## TODO list
+ Implement home-all feature.


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.
