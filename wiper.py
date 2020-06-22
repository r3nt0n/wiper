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

import os, sys, platform, time
import argparse
from shutil import rmtree
from socket import gethostname

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
    parser.add_argument('-r', '--root-path', action='store', metavar='root_path',
                        dest='root_path', type=str, default=False,
                        help='set a custom root path')
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
    print(u'  | [{}1{}] Wipe all free space in a choosen partition         |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}2{}] Wipe a single file/all files under a choosen path  |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +-- {}AUTO SEARCH MODE{} ------------------------------------+'.format(headers_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}3{}] Wipe my temporal directory                         |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}4{}] Wipe my personal directory (includes tempdir)      |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +-- {}AUTO SEARCH MODE (elevated privileges){} --------------+'.format(headers_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}5{}] Wipe all users temporal directories                |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}6{}] Wipe all users personal directories                |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  | [{}7{}] Wipe all swap partitions/pagination files          |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +--------------------------------------------------------+'); time.sleep(delay_per_line)
    print(u'  | [{}0{}] Exit                                               |'.format(options_color,color.END)); time.sleep(delay_per_line)
    print(u'  +--------------------------------------------------------+\r\n'); time.sleep(delay_per_line)

def is_empty(string):
    """Checks if a string is empty.
       Returns True or False
    """
    empty = False
    if len(str(string)) == 0: empty = True
    return empty

def set_root_path():
    print(u'  {}[!]{} System detected: {}{}{} (running {}{}{}) '.format(color.ORANGE, color.END,
                                                                        color.ORANGE, gethostname(), color.END,
                                                                        color.PURPLE, platform.system(), color.END))
    print(u'  {}[!]{} By default, {}auto-search{} mode targets the booted OS.'.format(color.ORANGE, color.END,
                                                                                      color.PURPLE,color.END))
    print(u'  {}[!]{} To wipe an unbooted system, you can provide the root'.format(color.ORANGE,color.END))
    print(u'  {}[!]{} path where is mounted (e.g. /media/mydrive), or PRESS'.format(color.ORANGE, color.END))
    print(u'  {}[!]{} ENTER to continue...'.format(color.ORANGE, color.END))
    root_path = input(u'  {}[?]{} '.format(color.PURPLE, color.END))
    if not is_empty(root_path):
        os.chdir(root_path)
    return root_path
    
def wipe(files_to_wipe, path_to_remove):
    # Wipe each file
    counter = 0
    for f in files_to_wipe:
        wiped = wiper_ops.wipe_file(f)
        if wiped: counter += 1
    print('  {}[!]{} Files wiped: {}{}{}'.format(color.GREEN, color.END,color.PURPLE,counter,color.END))
    # Remove the empty tree if path given was a dir AFTER ALL OVERWRITES
    if os.path.isdir(path_to_remove):
        try:
            print('  {}[+]{} Removed empty tree (path given was a dir)'.format(color.GREEN, color.END))
            rmtree(path_to_remove)
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
        custom_root_path = args.root_path
        # Print help and exit when runs without args
        if len(sys.argv) == 1: parser.print_help(sys.stdout); sys.exit(4)
        # Print help and exit when runs non-interactive without path
        if (not interactive and not path): parser.print_help(sys.stdout); sys.exit(4)
        if interactive:
            # Clear screen and print banner with options in interactive mode
            os_ops.clear()
            banner()
            custom_root_path = set_root_path()
            print(u'\r\n  {}[+]{} Your current working directory is:'.format(color.ORANGE, color.END))
            print(u'  {}[+]{} {}{}{}'.format(color.ORANGE, color.END, color.ORANGE, os.getcwd(), color.END))
        while True:
            # Get opt and check it
            opt = input(u'\r\n  {}[?]{} Choose an option [{}0-9{}]: '.format(color.PURPLE,color.END,color.ORANGE,color.END))
            # 0. Wipes all free space in the given paths
            if opt == '1':
                # Get the path from user input
                path = input(u'  {}[?]{} Enter the path you want to wipe: '.format(color.PURPLE,color.END))
                status = wiper_ops.wipe_free_space(path)
                if status == 0:
                    print(u'  {}[+]{} The free space was succesfully wiped.'.format(color.GREEN, color.END))
                else:
                    print(u'  {}[!]{} An error has occurred'.format(color.RED, color.END))
            # 1. Secure delete all data in the given path
            elif opt == '2':
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
               
            elif opt == '3':
                pass
            elif opt == '4':
                pass
            elif opt == '5':
                pass
            elif opt == '6':
                pass
            elif opt == '7':
                print('  {}[-]{} Looking for swap/pagefiles...'.format(color.ORANGE, color.END))
                swaplist = os_ops.get_swaps(custom_root_path)
                if not swaplist:
                    print(u'  {}[!]{} ERROR: Any swap partition or pagefile found'.format(color.RED, color.END))
                    if custom_root_path:
                        print(u'  {}[!]{} Try to run wiper booted on the target system'.format(color.ORANGE, color.END))
                if (type(swaplist) == str and swaplist.startswith(':ERR:')):
                    msg = swaplist.split(':ERR:')[1]
                    print(u'  {}[!]{} ERROR: {}'.format(color.ORANGE, color.END, msg))
                else:
                    print(u'  {}[+]{} {} swap/pagefiles founded'.format(color.PURPLE, color.END,len(swaplist)))
                    for swap in swaplist:
                        print(u'  {}[+]{} {}'.format(color.ORANGE, color.END,swap))
                    confirm = input(u'  {}[?]{} Do you want to confirm? (y/n) > '.format(color.PURPLE,color.END))
                    if (confirm.lower().startswith('y')):
                        if (os.name == 'nt' or custom_root_path):
                            for swap in swaplist:
                                files_to_wipe = (swap)  # Converts to tuple to be iterable inside wipe
                                wipe(files_to_wipe, path_to_remove=False)
                        elif (os.name == 'posix'):
                            for swap in swaplist:
                                status = wiper_ops.dd_random_wipe(swap)
                                if str(status) == '0':
                                    print(u'  {}[+]{} {}{}{} was succesfully wiped.'.format(color.GREEN,color.END,
                                                                                            color.PURPLE,swap,color.END))


            elif opt == '0':
                interactive = False
            else:
                print(u'  {}[!]{} Incorrect option.'.format(color.RED, color.END))
                continue
            if not interactive:
                break


if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

