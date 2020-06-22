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

import os, subprocess, shlex
from pathlib import Path

# wmi impoted in OS systems

################################################################################

def clear():
    """Clear the screen."""
    os.system(['clear', 'cls'][os.name == 'nt'])


def find_files(root_path, files_to_exclude=()):
    """Find files recursively from the given root_path. Special directories/files,
       like the script absolute path, can be excluded.
       Returns a list of files, including the absolute path of each one.
       Arguments:
       root -- root directory where it begins to search.
       files_to_exclude -- (optional) list of absolute path to files that will
                           be excluded from the return list
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

def get_default_root_system():
    """Gets the actual root path to the drive which contains the OS that is
       mounted, (e.g. 'C:' in Win (tipically), '/' in Linux.
       Returns a Path-object pointing to the root system
    """
    root = False
    if os.name == 'posix':
        root = '/'
    elif os.name == 'nt':
        root = '%SYSTEMDRIVE%'
    return Path(root)

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(u'{}'.format(output.strip()))
    rc = process.poll()
    return rc

def get_swaps(root_system=False):
    """Interacts with mounted/umounted  operative systems and search paths
       relatives to swap files/partitions.
       Returns a list with swap partitions founded (Linux) or pagefile paths (Win)
       Returns an empty list (implicit False) in case of any files founded
       Returns :ERR: follows by a description in case of error in the arg provide
       Arguments:
       root_system -- optional arg, if the target OS is umounted, you should
                      provide a root path to that system
    """
    swap_dirs = []
    # root_system provided and is a valid path, checking default path in Win (Linux don't supported)
    if os.path.isdir(root_system):
        default_pagefile_name = 'pagefile.sys'
        default_pagefile_path = Path(root_system) / default_pagefile_name
        swap_dirs = find_files(default_pagefile_path)
    # root_system provided but not a valid path (returns ERROR)
    elif root_system:
        swap_dirs = ':ERR:root_system should be an accesible dir - check path and permissions.'
    # root_system NOT provided, checking booted system info
    else:
        root_system_path = get_default_root_system()
        if os.name == 'posix':
            swaps_path = root_system_path / 'proc/swaps'
            p = subprocess.run('cat {}'.format(swaps_path), stdout=subprocess.PIPE,
                               text=True, shell=True, check=True)
            swaps = p.stdout.split('\n')[1:-1]
            for swap in swaps:
                swap_dirs.append(swap.split(' ')[0])
        elif os.name == 'nt':
            import wmi  # Importing WMI only on Windows machines
            pagefiles = wmi.WMI()
            for pf in pagefiles.Win32_Pagefile():
                swap_dirs.append(pf.Caption)
    return swap_dirs

def get_personal_dir(root='/'):
    """Interacts with the OS (Win/Linux) to get paths relatives to personal
       directories and swap files/partitions.
       Returns a list with personal directories founded
    """
    if os.name == 'posix':
        personal_dirs = ['$HOME']
    elif os.name == 'nt':
            personal_dirs = ['%USERPROFILE%', '%HOMEDRIVE%', '%HOMEPATH%']

if __name__ == '__main__':
    # Tests
    files_to_exclude = os.path.abspath(__file__)
    filelist = find_files('./*', files_to_exclude)
    print(filelist)

