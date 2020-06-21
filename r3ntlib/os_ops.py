#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n
# https://github.com/r3nt0n/wiper

"""
os_ops.py - kit of custom presets OS operations module
"""

name        = 'r3ntlib/os_ops.py'
__author__  = 'r3nt0n'
__version__ = '1.0'
__status__  = 'Development'

import os, subprocess
from pathlib import Path

# wmi impoted in OS systems

################################################################################

def clear():
    """Clear the screen."""
    os.system(['clear', 'cls'][os.name == 'nt'])


def find_files(root_path, files_to_exclude):
    """Find files recursively from the given root_path. The script absolute path
       can be excluded.
       Returns a list of files, including the absolute path of each one.
       Arguments:
       root -- root directory where it begins to search.
       files_to_exclude -- list of absolute path to files that will be excluded
                           from the return list.
    """
    files_list = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            exclude = False
            for file_excluded in files_to_exclude:
                if os.path.abspath(name) == file_excluded:
                    exclude = True
                    break   # Don't keep testing files excluded if it matches one
            if not exclude:
                files_list.append(Path(root) / name)
    return files_list


def get_variable_paths():
    """Interacts with the OS (Win/Linux) to get paths relatives to personal
       directories and swap files/partitions.
       Returns a tuple ([personal_dirs], [swap_dirs]) and each element is a list.
    """
    personal_dirs = []
    swap_dirs = []
    if os.name == 'posix':
        personal_dirs = ['$HOME']
        p = subprocess.run('cat /proc/swaps', stdout=subprocess.PIPE,
                           text=True, shell=True, check=True)
        swaps = p.stdout.split('\n')[1:-1]
        for swap in swaps:
            swap_dirs.append(swap.split(' ')[0])
    elif os.name == 'nt':
        import wmi  # Importing WMI only in Windows OS
        personal_dirs = ['%USERPROFILE%', '%HOMEDRIVE%', '%HOMEPATH%']
        pagefiles = wmi.WMI()
        for pf in pagefiles.Win32_Pagefile():
            swap_dirs.append(pf.Caption)
    return personal_dirs, swap_dirs


if __name__ == '__main__':
    # Tests
    files_to_exclude = os.path.abspath(__file__)
    filelist = find_files('./*', files_to_exclude)
    print(filelist)