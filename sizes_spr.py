#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def read2_to_int(f):
    a = f.read(1)
    b = f.read(1)
    return ord(a) + ord(b)*256


def main(name):
    f = file(name)
    seek = 8
    f.seek(seek)
    while 1:
        sizex = read2_to_int(f)
        sizey = read2_to_int(f)
        sizedata = read2_to_int(f)
        if sizedata == 65535:
            break
        print "(%s, %s)," % (sizex, sizey),
        seek += 6 + sizedata
        f.seek(seek)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Need file"
    else:
        main(sys.argv[1])