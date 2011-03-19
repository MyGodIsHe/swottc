#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    import OpenGL
except ImportError:
    print "Need install OpenGL"
    sys.exit()

from optparse import OptionParser
from window import Window


if __name__ == '__main__':
    usage = "usage: %prog -d 3 -c 50 -r 50"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--density", dest="density", type="int", help="The population density of 1 to 100", default=20)
    parser.add_option("-c", "--cols", dest="cols", type="int", help="Number of cells along the horizontal", default=20)
    parser.add_option("-r", "--rows", dest="rows", type="int", help="Number of cells along the vertical", default=20)

    (options, args) = parser.parse_args()
    if options.density < 1 or options.density > 100:
        parser.error("density of 1 to 100")
    if options.cols < 3 or options.cols > 1000:
        parser.error("cols of 3 to 1000")
    if options.rows < 3 or options.rows > 1000:
        parser.error("rows of 3 to 1000")
    window = Window(log='debug.log',
                    colors='./rgb.txt',
                    options=options,
                    args=args)
    window.loop()