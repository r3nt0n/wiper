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
__version__ = '0.6~beta'
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

    parser.add_argument('-i', '--interactive',action='store_true',dest='interactive',default=False,
                        help='interactive mode, the script will guide you')
    parser.add_argument('-f', '--free',action='store',dest='free',type=str,default=False,metavar='path',
                        help='wipe all free space on given path')
    parser.add_argument('-p', '--path',action='store',dest='path',type=str, default=False,metavar='path',
                        help='path to dir/file you want to wipe')

    parser.add_argument('-r', '--root',action='store',dest='root_path',type=str,default=False,
                        metavar='path',help='set a custom root path if you want to wipe with auto-search modes an unbooted system (e.g. /media/drive)')
    parser.add_argument('-t', '--temp', action='store_true',dest='temp',default=False,
                        help='auto-search mode: locate actual user temp directory and wipes it')
    parser.add_argument('-u', '--home', action='store_true',dest='home',default=False,
                        help='auto-search mode: locate actual user home directory and wipes it')
    parser.add_argument('-T', '--temp-all', action='store_true',dest='temp_all',default=False,
                        help='auto-search mode: locate all users temp directory and wipes it')
    parser.add_argument('-U', '--home-all', action='store_true',dest='home_all',default=False,
                        help='auto-search mode: locate all users home directory and wipes it')
    parser.add_argument('-s', '--swaps', action='store_true',dest='swaps',default=False,
                        help='auto-search mode: locate swap partitions/pagefiles and wipes it (be careful: UUID swap partitions also will be wiped)')
    return parser

def banner():
    headers_color = color.PURPLE
    options_color = color.ORANGE
    appname_color = color.PURPLE
    author_color = color.ORANGE
    delay_per_line = 0.02
    time.sleep(delay_per_line*2)
    print(u"             __________                                  "); time.sleep(delay_per_line)
    print(u"           .'----------`.        +------+                "); time.sleep(delay_per_line)
    print(u"           | .--------. |        | -- - |                "); time.sleep(delay_per_line)
    print(u"           | |########| |       _|______|_               "); time.sleep(delay_per_line)
    print(u"           | |########| |      /__________\              "); time.sleep(delay_per_line)
    print(u"  .--------| `--------' |------|1 -=====- |----------------."); time.sleep(delay_per_line)
    print(u"  |        `----,-.-----'      |o =w1p3r= |                |"); time.sleep(delay_per_line)
    print(u"  |       ______|_|_______     |__________|                |"); time.sleep(delay_per_line)
    print(u"  |      /  %%%%%%%%%%%%  \     | | | | |                  |"); time.sleep(delay_per_line)
    print(u"  |     /  %%%%%%%%%%%%%%  \    | | | | |    wiper.py {}{}{}  |".format(appname_color,(__version__)[0:3],color.END)); time.sleep(delay_per_line)
    print(u"  |     ^^^^^^^^^^^^^^^^^^^^                       {}{}{}  |".format(author_color,__author__,color.END)); time.sleep(delay_per_line)
    print(u"  +--------------------------------------------------------+"); time.sleep(delay_per_line)
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
    print(u'  {}[!]{} path where is mounted (e.g.: /media/mydrive).'.format(color.ORANGE, color.END))
    print(u'  {}[!]{} SET a custom root path or PRESS ENTER to continue...'.format(color.ORANGE, color.END))
    root_path = False
    user_input = input(u'  {}[?]{} '.format(color.PURPLE, color.END))
    if os.path.isdir(user_input):
        root_path = user_input
    if not is_empty(user_input):
        try: os.chdir(user_input)
        except Exception as exception: print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
    return root_path
    
def wipe(path, exclude_script=True):
    status = 3
    if not exclude_script:
        files_to_wipe = os_ops.find_files(path)
    else:
        # Get actual script absolute path to exclude from deletion task
        script_abspath = os.path.abspath(__file__)
        # Get all files included in the given path
        files_to_wipe = os_ops.find_files(path, script_abspath)
    if not files_to_wipe:
        print(u'  {}[!]{} ERROR: No files found'.format(color.RED, color.END))
        status = 2
    else:
        print(u'  {}[+]{} Files found: {}{}{}'.format(color.GREEN, color.END, color.PURPLE, len(files_to_wipe), color.END))
        # Wipe each file
        counter = 0
        for f in files_to_wipe:
            wiped = wiper_ops.wipe_file(f)
            if wiped: counter += 1
        print(u'  {}[+]{} Files wiped: {}{}{}'.format(color.GREEN, color.END,color.PURPLE,counter,color.END))
        # Remove the empty tree if path given was a dir AFTER ALL OVERWRITES
        if os.path.isdir(path):
            try:
                print(u'  {}[+]{} Removed empty tree (path given was a dir)'.format(color.GREEN, color.END))
                rmtree(path)
                status = 0
            except Exception as exception: print('{}  [!]{} ERROR: {}'.format(color.RED,color.END,exception)); status=1
    return status


def main():
    if (os.name != 'posix' and os.name != 'nt'):
        print(u'{}[!]{} Incompatible Operative System detected. Exiting...'.format(color.RED, color.END))
        sys.exit(5)
    else:
        # Load arguments
        parser = read_args()
        args = parser.parse_args()
        interactive = args.interactive
        wipe_free_arg = args.free
        path = args.path
        custom_root_path = args.root_path
        wipe_temp_arg = args.temp
        wipe_home_arg = args.home
        wipe_temp_all_arg = args.temp_all
        wipe_home_all_arg = args.home_all
        wipe_swaps_arg = args.swaps
        # Print help and exit when runs without args
        if len(sys.argv) == 1: parser.print_help(sys.stdout); sys.exit(4)
        # Print help and exit when runs non-interactive without path
        if (not interactive and not wipe_free_arg and not path and not wipe_temp_arg and not wipe_home_arg and not wipe_temp_arg and not wipe_temp_all_arg and not wipe_swaps_arg):
            parser.print_help(sys.stdout); sys.exit(4)
        if interactive:
            # Clear screen and print banner with options in interactive mode
            os_ops.clear()
            banner()
            custom_root_path = set_root_path()
            print(u'\r\n  {}[+]{} Your current working directory is:'.format(color.ORANGE, color.END))
            print(u'  {}[+]{} {}{}{}'.format(color.ORANGE, color.END, color.ORANGE, os.getcwd(), color.END))
        while True:
            opt = ''
            if interactive:
                # Get opt and check it
                path = ''
                opt = input(u'\r\n  {}[?]{} Choose an option [{}0-9{}]: '.format(color.PURPLE,color.END,color.ORANGE,color.END))
            # 0. Wipes all free space in the given paths
            if (opt == '1' or wipe_free_arg):
                # Get the path from user input
                if wipe_free_arg:
                    path = wipe_free_arg
                else:
                    path = input(u'  {}[?]{} Enter the path you want to wipe all free space: '.format(color.PURPLE,color.END))
                status = wiper_ops.wipe_free_space(path)
                if status == 0:
                    print(u'  {}[+]{} The free space was succesfully wiped.'.format(color.GREEN, color.END))
                else:
                    print(u'  {}[!]{} An error has occurred'.format(color.RED, color.END))
            # 1. Secure delete all data in the given path
            elif (opt == '2' or path):
                # Get the path from user input
                if not path: path = input(u'  {}[?]{} Enter the path you want to wipe: '.format(color.PURPLE, color.END))
                wipe(path)

            elif (opt == '3' or wipe_temp_arg):
                print(u'  {}[x]{} This feature is not still implemented.'.format(color.ORANGE, color.END))
                continue
            # Wipes user personal dir
            elif (opt == '4' or wipe_home_arg):
                personal_dirs = os_ops.get_personal_dirs()
                if not personal_dirs:
                    print(u'  {}[!]{} ERROR: Any home directory found'.format(color.RED, color.END))
                else:
                    print(u'  {}[+]{} {}{}{} personal dirs found\r\n'.format(color.ORANGE, color.END, color.ORANGE,
                                                                   len(personal_dirs), color.END))
                    for pdir in personal_dirs:
                        print(u'  {}[+]{} [{}{}{}]  {}'.format(color.GREEN, color.END,
                                                             color.PURPLE,personal_dirs.index(pdir),
                                                             color.END,pdir))
                if len(personal_dirs) > 0:
                    if len(personal_dirs) == 1:
                        pdir = personal_dirs[0]
                    else:
                        pdir = input(u'\r\n  {}[?]{} Choose the one you want to wipe [{}0-{}{}] '.format(color.PURPLE,color.END,
                                                                                                  color.ORANGE,str(len(personal_dirs)-1),
                                                                                                  color.END))
                        if (type(pdir) is not int or int(pdir) >= len(personal_dirs)):
                            print(u'  {}[!]{} ERROR: Bad option choosen'.format(color.RED, color.END))
                            continue  # Back to menu
                    wipe(pdir)
            elif (opt == '5' or wipe_temp_all_arg):
                print(u'  {}[x]{} This feature is not still implemented.'.format(color.ORANGE, color.END))
                continue
            elif (opt == '6' or wipe_home_all_arg):
                print(u'  {}[x]{} This feature is not still implemented.'.format(color.ORANGE, color.END))
                continue
            # Wipes swaps/pagefiles
            elif (opt == '7' or wipe_swaps_arg):
                print(u'  {}[-]{} Searching swap/pagefiles...'.format(color.ORANGE, color.END))
                swaplist = os_ops.get_swaps(custom_root_path)
                if not swaplist:
                    print(u'  {}[!]{} ERROR: Any swap partition or pagefile found'.format(color.RED, color.END))
                    if custom_root_path:
                        print(u'  {}[!]{} Try to run wiper booted on the target system'.format(color.ORANGE, color.END))
                if (type(swaplist) == str and swaplist.startswith(':ERR:')):
                    msg = swaplist.split(':ERR:')[1]
                    print(u'  {}[!]{} ERROR: {}'.format(color.ORANGE, color.END, msg))
                else:
                    print(u'  {}[+]{} {} swap/pagefiles found\r\n'.format(color.PURPLE, color.END,len(swaplist)))
                    for swap in swaplist:
                        print(u'  {}[+]{} {}'.format(color.ORANGE, color.END,swap))
                    confirm = input(u'  {}[?]{} Do you want to confirm? (y/n) > '.format(color.PURPLE,color.END))
                    if (confirm.lower().startswith('y')):
                        if (os.name == 'nt' or custom_root_path):
                            wipe(swaplist)
                        elif (os.name == 'posix'):
                            for swap in swaplist:
                                status = wiper_ops.dd_linux_wipe(swap)
                                if str(status) == '0':
                                    print(u'  {}[+]{} {}{}{} was succesfully wiped.'.format(color.GREEN,color.END,
                                                                                            color.PURPLE,swap,color.END))

            elif (opt == '0' or opt == 'quit' or opt == 'exit'):
                interactive = False
            else:
                print(u'  {}[!]{} Incorrect option.'.format(color.RED, color.END))
                continue
            if not interactive:
                break


if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print(u'\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

