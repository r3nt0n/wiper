#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n
# https://github.com/r3nt0n/wiper

"""
wiper_ops.py - wiper core module
"""

name        = 'r3ntlib/wiper_ops.py'
__author__  = 'r3nt0n'
__version__ = '0.5~beta'
__status__  = 'Development'

import os, subprocess
from shutil import disk_usage, rmtree
from pathlib import Path
from random import getrandbits

from r3ntlib.os_ops import run_command
from r3ntlib.color import color

################################################################################

def random_wipe(path, mode, size_to_write):
    """Overwrite the given path with n random bytes (n is the size given in bytes)
           Returns a status code:
           0 - OK, 1-Space wasn't even filled randomly, 2-Space wasn't secure delete
           Arguments:
           path -- root directory where it begins to search.
           mode -- 'ab+' for wipe free space in the given path,
                   'wb' to overwrite an existing file
        """
    status = 0
    try:
        print(u'  {}[+]{} Overwriting {}{}{} ({}{}{} bytes)'.format(color.ORANGE,color.END,
                                                                    color.ORANGE, path, color.END,
                                                                    color.PURPLE, size_to_write, color.END))
        print(u'  {}[+]{} Starting one-pass random wipe...'.format(color.ORANGE, color.END))
        pointer = 0
        with open(path, mode) as dummy_file:
            while size_to_write > 0:
                randbyte = bytearray(getrandbits(8) for _ in range(1))
                dummy_file.write(randbyte)
                size_to_write -= 1
                if mode == 'wb':
                    pointer += 1
                    dummy_file.seek(pointer)
        print('{}  [+]{} {}{}{} was randomly overwritten'.format(color.PURPLE, color.END,
                                                                 color.ORANGE, path, color.END))
        try:
            if os.path.isfile(path):
                os.remove(path)
            print('  {}[-]{} {}{}{} was {}succesfully{} wiped'.format(color.GREEN, color.END,
                                                                      color.ORANGE, path, color.END,
                                                                      color.GREEN, color.END))
        except Exception as exception:
            status = 2
            print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
    except Exception as exception:
        status = 2
        print('{}  [!]{} ERROR: {}'.format(color.RED,color.END,exception))
    return status

def dd_random_wipe(linux_path):
    '''Random wipe using dd tool on Linux OS.
       Returns 6 if uncompatible operative system is detected
       Returns 4 if error triggered trying to run subprocess
       Returns standard dd return-codes if task was completed (0)
    '''
    status = 6
    if os.name == 'posix':
        try:
            bytes_to_write = disk_usage(linux_path)[2]
            print('  {}[+]{} Starting to wipe {}{}{} ({}{}{} bytes) with dd tool...\r\n'.format(color.ORANGE, color.END,
                                                                                            color.ORANGE,linux_path,color.END,
                                                                                            color.PURPLE,bytes_to_write,color.END))
            command = 'dd if=/dev/urandom of={} bs=4096 status=progress'.format(linux_path)
            status = run_command(command)
        except Exception as exception:
            status = 4
            print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
    return status



################################################################################

def wipe_free_space(path):
    """Fill free space disk with random bytes and secure delete the file
       previously created.
       Returns a status code:
       0 - OK, 1-Space wasn't even filled randomly, 2-Space wasn't secure delete
       Arguments:
       path -- root directory where it begins to search.
    """
    tempfile = os.path.join(path,'00000001')
    try:
        free_space = disk_usage(path)[2]
        random_wipe(tempfile, 'ab+', free_space)
    except Exception as exception:
        print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
    finally:
        # Makes sure to clean-up tempfile
        try: os.remove(tempfile)
        except: pass

def wipe_file(path):
    """Wipe a single file
       Returns True or False regarding if it was succesfuly deleted or not.
           Arguments:
           path -- path to file
    """
    try:
        bytesize_to_write = os.stat(path).st_size
        random_wipe(path, 'wb', bytesize_to_write)
        status = True
    except Exception as exception:
        print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
        status = False
    return status

