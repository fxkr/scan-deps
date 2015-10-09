#!/usr/bin/env python

import os
import re
import sys


def find_deps_in_file(depfilepath):
    with open(depfilepath) as file:
        for line in file:
            if ': ' in line: line = line.split(': ', 1)[1]
            line = line.strip('\r\n \\')
            line = line.split(' ')
            line = filter(None, line)
            for dep in line:
                yield dep

def find_depfiles(searchpath):
    for dirpath, dirnames, filenames in os.walk(searchpath):
        for filename in filenames:
            if filename.startswith("."):
                continue
            if not filename.endswith(".d"):
                continue
            fullpath = os.path.join(searchpath, dirpath, filename)
            yield fullpath

def find_deps_in_path(searchpath, basepath, ignore_abs):
    for depfilepath in find_depfiles(searchpath):
        depfiledir = os.path.dirname(depfilepath)
        for dep in find_deps_in_file(depfilepath):

            path = os.path.normpath(os.path.join(basepath, dep))
            path = os.path.realpath(path)

            # Relative path?
            if path.startswith(os.path.realpath(searchpath) + "/"):
                path = os.path.relpath(path, searchpath)
                yield path

            # Absolute path?
            elif not ignore_abs:
                yield path

def main(searchpath, basepath, exclude):
    for entry in sorted(set(find_deps_in_path(searchpath, basepath))):
        if entry not in exclude:
            print(entry)


if __name__ == '__main__':
    main(".", "hostapd", exclude=['hostapd/main.c', 'hostapd/hostapd_cli.c'], ignore_abs=True)

