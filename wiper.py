#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n
# https://github.com/r3nt0n/wiper

"""
wiper.py - wiper run script

EXIT CODE 0 - OK
EXIT CODE 3 - KEYBOARD INTERRUPT
EXIT CODE 4 - FEW ARGUMENTS PROVIDED
EXIT CODE 5 - INCOMPATIBLE OPERATIVE SYSTEM

Wiper is a set of tools to perform secure destruction of sensitive virtual data, temporary files and swap memories.

## Features
+ MANUAL wipe selection:
You can wipe: single files, whole directories, whole free space in partitions.
+ AUTO wipe selection:
An automatic selection of paths to wipe, relatives to personal directories and swap data.
If you run it with the OS target unmounted, you should provide the root path/mount point to that system.
"""


name        = 'wiper.py'
__author__  = 'r3nt0n'
__version__ = '0.5'
__status__  = 'Development'

################################################################################

import os, sys, time
import argparse
from shutil import rmtree

from r3ntlib import wiper_ops
from r3ntlib import os_ops
from r3ntlib.color import color

################################################################################
# ARGS DEFINITION
################################################################################
def read_args():
    parser = argparse.ArgumentParser(description='set of tools to perform secure destruction of sensitive virtual data, \
                                                  temporary files and swap memories.. Absolute and relative paths are \
                                                  allowed, but no wildcards. Find more info at https://github.com/r3nt0n/wiper')

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='interactive mode, the script will guide you')

    parser.add_argument('-w', '--free-space', action='store_true',
                        help='wipe all free space on given path')

    parser.add_argument('-p', '--path', action='store', metavar='path',
                        dest='path', type=str, default=False,
                        help='path to partition/file you want to wipe (required in non-interactive mode)')
    return parser

def banner():
    headers_color = color.PURPLE
    options_color = color.ORANGE
    appname_color = color.PURPLE
    author_color = color.ORANGE
    delay_per_line = 0.02
    time.sleep(delay_per_line*2)
    print("             __________                                  "); time.sleep(delay_per_line)
    print("           .'----------`.        +------+                "); time.sleep(delay_per_line)
    print("           | .--------. |        | -- - |                "); time.sleep(delay_per_line)
    print("           | |########| |       _|______|_               "); time.sleep(delay_per_line)
    print("           | |########| |      /__________\              "); time.sleep(delay_per_line)
    print("  .--------| `--------' |------|1 -=====- |----------------."); time.sleep(delay_per_line)
    print("  |        `----,-.-----'      |o =w1p3r= |                |"); time.sleep(delay_per_line)
    print("  |       ______|_|_______     |__________|                |"); time.sleep(delay_per_line)
    print("  |      /  %%%%%%%%%%%%  \     | | | | |                  |"); time.sleep(delay_per_line)
    print("  |     /  %%%%%%%%%%%%%%  \    | | | | |    wiper.py {}{}{}  |".format(appname_color,__version__,color.END)); time.sleep(delay_per_line)
    print("  |     ^^^^^^^^^^^^^^^^^^^^                       {}{}{}  |".format(author_color,__author__,color.END)); time.sleep(delay_per_line)
    print("  +--------------------------------------------------------+"); time.sleep(delay_per_line)
    print(u'  +-- {}MANUAL SELECTION MODE{} -------------------------------+'.format(headers_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}0{}] Wipe all free space in a choosen partition         |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}1{}] Wipe a single file/all files under a choosen path  |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +-- {}AUTO SEARCH MODE{} ------------------------------------+'.format(headers_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}2{}] Wipe my temporal directory                         |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}3{}] Wipe my personal directory (includes tempdir)      |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +-- {}AUTO SEARCH MODE (elevated privileges){} --------------+'.format(headers_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}4{}] Wipe all users temporal directories                |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}4{}] Wipe all users personal directories                |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}5{}] Wipe all swap partitions/pagination files          |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +--------------------------------------------------------+'); time.sleep(delay_per_line)
    print(u'  | [{}9{}] Exit                                               |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +--------------------------------------------------------+'); time.sleep(delay_per_line)
    
def wipe(files_to_wipe, path):
    # Wipe each file
    counter = 0
    for f in files_to_wipe:
        wiped = wiper_ops.wipe_file(f)
        if wiped: counter += 1
    print('  {}[!]{} Files wiped: {}{}{}'.format(color.GREEN, color.END,color.PURPLE,counter,color.END))
    # Remove the empty tree if path given was a dir AFTER ALL OVERWRITES
    if os.path.isdir(path):
        try:
            print('  {}[+]{} Removed empty tree (path given was a dir)'.format(color.GREEN, color.END))
            rmtree(path)
        except Exception as exception: print('{}  [!]{} ERROR: {}'.format(color.RED,color.END,exception))


def main():
    if (os.name != 'posix' and os.name != 'nt'):
        print(u'{}[!]{} Incompatible Operative System detected. Exiting...'.format(color.RED, color.END))
        sys.exit(5)
    else:
        # Load arguments
        parser = read_args()
        args = parser.parse_args()
        interactive = args.interactive
        path = args.path
        # Print help and exit when runs without args
        if len(sys.argv) == 1: parser.print_help(sys.stdout); sys.exit(4)
        # Print help and exit when runs non-interactive without path
        if (not interactive and not path): parser.print_help(sys.stdout); sys.exit(4)
        if interactive:
            # Clear screen and print banner with options in interactive mode
            os_ops.clear()
            banner()
            print(u'\r\n  {}[+]{} Your current working directory is:'.format(color.ORANGE, color.END))
            print(u'  {}[+]{} {}{}{}'.format(color.ORANGE, color.END, color.ORANGE, os.getcwd(), color.END))
        while True:
            # Get opt and check it
            opt = input(u'\r\n  {}[?]{} Choose an option [{}0-4{}]: '.format(color.PURPLE,color.END,color.ORANGE,color.END))
            # 0. Wipes all free space in the given paths
            if opt == '0':
                # Get the path from user input
                path = input(u'  {}[?]{} Enter the path you want to wipe: '.format(color.PURPLE,color.END))
                status = wiper_ops.wipe_free_space(path)
                if status == 0:
                    print(u'  {}[+]{} The free space was succesfully wiped.'.format(color.GREEN, color.END))
                else:
                    print(u'  {}[!]{} An error has occurred'.format(color.RED, color.END))
            # 1. Secure delete all data in the given path
            elif opt == '1':
                # Get the path from user input
                path = input(u'  {}[?]{} Enter the path you want to wipe: '.format(color.PURPLE, color.END))
                # Get actual script absolute path to exclude from a deletion task
                script_abspath = os.path.abspath(__file__)
                # Get all files included in the given path
                files_to_wipe = os_ops.find_files(path, script_abspath)
                if not files_to_wipe:
                    print(u'  {}[!]{} ERROR: No files found'.format(color.RED, color.END))
                    continue
                print('  {}[!]{} Files founded: {}{}{}'.format(color.GREEN, color.END, color.PURPLE, len(files_to_wipe), color.END))
                wipe(files_to_wipe, path)
               
            elif opt == '2':
                pass
            elif opt == '3':
                pass
            elif opt == '4':
                pass
            elif opt == '5':
                if os.name == 'nt':
                    pass
                if os.name == 'posix':
                    pass
                    # subprocess -> dd if=/dev/random of=$swappartition
            # ...
            # 2. Get variable paths relatives to personal directories, swap file/partitions
            elif opt == 'get-paths':
                personal_dirs, swap_dirs = os_ops.get_variable_paths()
                # ...
            elif opt == '9':
                interactive = False
            else:
                print(u'  {}[!]{} Incorrect option.'.format(color.RED, color.END))
                continue
            if not interactive:
                break


if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

