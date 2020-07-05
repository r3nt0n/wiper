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


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Found in: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

################################################################################

def wipe_bytes(path, mode, size_to_write, method='r'):
    """Overwrite the given path with n random bytes (n is the size given in bytes)
           Returns a status code:
           0 - OK, 1-Space wasn't even filled randomly, 2-Space wasn't secure delete
           Arguments:
           path          -- root directory where it begins to search.
           mode          -- 'ab+' for wipe free space in the given path,
                            'wb' to overwrite an existing file
           size-to-write -- size in bytes to overwrite
           methods       -- if tuple contains: r -> random, z -> zeros, o -> ones
        """
    status = 1
    try:
        for m in method:
            if m == 'z':
                print(u'  {}[-]{} Starting one-pass zeros wipe...'.format(color.ORANGE, color.END))
                overwritebyte = b'\x00'
            elif m == 'o':
                print(u'  {}[-]{} Starting one-pass ones wipe...'.format(color.ORANGE, color.END))
                overwritebyte = b'\xff'
            else:
                print(u'  {}[-]{} Starting one-pass random wipe...'.format(color.ORANGE, color.END))

            pointer = 0
            with open(path, mode) as dummy_file:
                #while size_to_write > 0:
                for j in progressBar(range(1,size_to_write), prefix='Progress:', suffix='Complete', length=50):
                    if m == 'r':
                        overwritebyte = bytearray(getrandbits(8) for _ in range(1))
                    dummy_file.write(overwritebyte)
                    #size_to_write -= 1
                    if mode == 'wb':
                        pointer += 1
                        dummy_file.seek(pointer)
        status = 0
        print('\r\n  {}[-]{} {}{}{} was {}succesfully{} wiped'.format(color.GREEN, color.END,
                                                                      color.ORANGE, path, color.END,
                                                                      color.GREEN, color.END))
    except Exception as exception:
        status = 2
        print('{}  [!]{} ERROR: {}'.format(color.RED,color.END,exception))

    finally:
        if (os.path.isfile(path) and status == 0):
            os.remove(path)

    return status

def dd_linux_wipe(linux_path, method='r'):
    '''Random wipe using dd tool on Linux OS.
       Returns 6 if uncompatible operative system is detected
       Returns 4 if error triggered trying to run subprocess
       Returns standard dd return-codes if task was completed (0)
    '''
    status = 6
    if os.name == 'posix':
        try:
            for m in method:
                bs = '1024'
                if m == 'z':
                    src = '/dev/zero'
                    print(u'  {}[-]{} Starting one-pass zeros wipe...'.format(color.ORANGE, color.END))
                elif m == 'o':
                    src = "<(yes $'\\ff' | tr -d \"\\n\")"
                    print(u'  {}[-]{} Starting one-pass ones wipe...'.format(color.ORANGE, color.END))
                else:
                    src = '/dev/urandom'
                    bs = '4096'
                    print(u'  {}[-]{} Starting one-pass random wipe...'.format(color.ORANGE, color.END))
                bytes_to_write = disk_usage(linux_path)[2]
                print('  {}[+]{} Starting to wipe {}{}{} ({}{}{} bytes) with dd tool...\r\n'.format(color.ORANGE, color.END,
                                                                                                color.ORANGE,linux_path,color.END,
                                                                                                color.PURPLE,bytes_to_write,color.END))
                command = 'dd if={} of={} bs={} status=progress'.format(src,linux_path,bs)
                status = run_command(command)
        except Exception as exception:
            status = 4
            print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
    return status



################################################################################

def wipe_free_space(path, method):
    """Fill free space disk with random bytes and secure delete the file
       previously created.
       Returns a status code:
       0 - OK, 1-Space wasn't even filled randomly, 2-Space wasn't secure delete
       Arguments:
       path -- root directory where it begins to search.
    """
    tempfile = os.path.join(path,'00000000.dummyfile')
    try:
        free_space = disk_usage(path)[2]
        wipe_bytes(tempfile, 'ab+', free_space, method)
    except Exception as exception:
        print('{}  [!]{} ERROR: {}'.format(color.RED, color.END, exception))
